import { Inter } from 'next/font/google'
import { clearFromSession, getFromStorage } from '@/lib/session-storage'
import React from 'react'
import { User } from '@/types/user'
import { useRouter } from 'next/router'
import dynamic from 'next/dynamic';
import Chart from '@/components/chart'
import { Box, Button, ChakraProvider, Divider, Flex, FormControl, HStack, Heading, Icon, Input, Select, Spacer, Text, VStack } from '@chakra-ui/react'
import { CalendarIcon } from '@chakra-ui/icons'
import Header from '@/components/heading'
import DateFilters from '@/components/date-filters'
import { color } from 'framer-motion'
import { title } from 'process'
import { verify } from 'crypto'

type ServerUsersAndGroups = {
  groupName:string,
  groupId:number,
  users:{id:number,name:string}[]
}



const inter = Inter({ subsets: ['latin'] })

const valueToDateMap:Record<string|number, any> = {
  1:'from the last 7 days',
  2: 'from the last 30 days',
  7: 'from the last 6 months',
  all: 'from all times'
}

  const  Home = function(props:any) {

  const user = getFromStorage('user') as User

  const [groups,setGroups] = React.useState<ServerUsersAndGroups[]>([])
  const [selectedGroup,setSelectedGroup] = React.useState<any>(null)
  const [selectedUser,setSelectedUser] = React.useState<any>(null)
  const [dataByCategories,setDataByCategories] = React.useState<(string | number)[][]>()
  const [dataByUserName,setDataByUserName] = React.useState<(string | number)[][]>()
  const [dataByMonth, setDataByMonth] = React.useState<(string | number)[][]>()
  const [dateFilter,setDateFilter]= React.useState<string | number>('all')
  const [isAdmin,setIsAdmin]= React.useState(false)
  const [totalExpeness,setTotalEpensess]= React.useState(0)
  const router=  useRouter()

  const onLogout = function(){
    router.push("/login")
    clearFromSession('user')
  }

  const getUserGroups = async function(){
    // Get data from server
    const res  = await fetch("/api/user-data",{
      method:"POST",
      body:JSON.stringify({
        userId:user.pk_id,
      })
  })  
  const {usersGroupsMap,isUserAdmin} = await res.json()
  setGroups(usersGroupsMap)
  setSelectedGroup(Object.keys(usersGroupsMap)[0])
  setIsAdmin(isUserAdmin)
  setSelectedUser("all")
  }

  const getProducts = async function(userId:string,groupId:string){
    const res  = await fetch("/api/expenses-per-category",{
      method:"POST",
      body:JSON.stringify({
        userId:userId === "all" ? null:userId,
        groupId,
        dateFilter
      })
  }) 
  const categoryAndAmountDic= await res.json()
  setDataByCategories(categoryAndAmountDic)
  }

  const getUserAmount = async function(userId:string,groupId:string){
    const res  = await fetch("/api/expenses-per-user",{
      method:"POST",
      body:JSON.stringify({
        groupId,
        dateFilter,
        userId:userId === "all" ? null:userId,
      })
  }) 
  const {userNameAndAmountDic,totalExpenses} = await res.json()
  setDataByUserName(userNameAndAmountDic)
  setTotalEpensess(totalExpenses)
  }

  const getDataByMonth = async function(userId:string,groupId:string){
    const res  = await fetch("/api/expenses-per-month",{
      method:"POST",
      body:JSON.stringify({
        groupId,
        userId:userId === "all" ? null:userId,
      })
  }) 
  const {monthAndAmount} = await res.json()
  console.log({monthAndAmount})
  setDataByMonth(monthAndAmount)
  }
  
  const onGroupSelect = function(e:React.ChangeEvent<HTMLSelectElement>){
    const groupId = e.target.value;
   setSelectedGroup(groupId)
     setSelectedUser("all")
  };

  const onUserSelect = function(e:React.ChangeEvent<HTMLSelectElement>){
    const userId = e.target.value;
   setSelectedUser(userId)
  };

  React.useEffect(()=>{
    if(!user){
      router.push("/home")
      return
    }
    getUserGroups()

  },[])

  React.useEffect(()=>{
    if(selectedGroup === null) return
      getProducts(selectedUser,selectedGroup)
      getUserAmount(selectedUser,selectedGroup)
      getDataByMonth(selectedUser,selectedGroup)
  },[selectedGroup,selectedUser,dateFilter])

  if(!user){
    return <div>Loading..</div>
  }

  console.log(dataByMonth);


  return (
   
        <main className={inter.className}>
          <Header isAdmin={isAdmin} user={user} onLogout={onLogout}/>

          <Flex padding="10px" alignItems={"center"}>
            <HStack spacing={5}>
              <Text textAlign={"left"} margin={2}>
                Groups:
              </Text>
              <Box w="150px">
                {/*Show Groups  */}
                <Select variant={"flushed"} size="sm" defaultValue={groups[selectedGroup]?.groupName} onChange={onGroupSelect}>
                {Object.values(groups)?.map((gr)=><option key={gr.groupId} value={gr.groupId}>{gr.groupName}</option>)}
                </Select>
              </Box>  

              <Text textAlign={"left"} margin={2}>
                Users:
              </Text>
              <Box w="150px">
                {/* Show Users */}
                <Select variant={"flushed"} size="sm" value={selectedUser} defaultValue={selectedUser} onChange={onUserSelect}>
                <option value="all">All</option>
                {groups[selectedGroup]?.users?.map((user)=><option key={user.id} value={user.id}>{user.name}</option>)}
                </Select>
              </Box>
            </HStack>
            <Spacer />

            <HStack spacing="5px">
              <CalendarIcon />
              <Text colorScheme='telegram' fontSize="sm">Date Filters: </Text>
              <DateFilters onChange={(date)=>setDateFilter(date)}/>
            </HStack>
          </Flex>

          <Text textAlign={"left"} margin={5} fontWeight="bold" textDecoration="underline">
              Here are your expenses {valueToDateMap[dateFilter]}:
          </Text>
          <Flex alignItems={"center"} padding={10} justifyContent={"space-evenly"}>
            {/*change top box to bar chart for user expenses*/}
              <Box>
              <Chart 
                type='Bar' 
                data={dataByUserName} 
                options={
                  {chart:{
                    title:"Expenses By User"}, 
                    series: {
                      0: { axis: "Temps" },
                    },
                    axes: {
                      y: {
                        Temps: { label: "Amount" },
                      }
                    }}} backgroundColor='white'/> 
              </Box>
              <Box>
                <div id="pie-chart">
                  <Chart type='PieChart' data={dataByCategories} options={{title:"Expenses By Category"}} backgroundColor='white'/> 
                </div>
              </Box>
          </Flex>
          <Text textAlign={"center"}>
              Total Expenses: {totalExpeness} NIS
          </Text>
          <Text textAlign={"left"} margin={5} fontWeight="bold" textDecoration="underline" paddingBottom={5}> 
              Here are your expenses per month:
          </Text>
          <Box width={1000} margin={'auto'}>
            <Chart type='Line' 
              data={dataByMonth} 
              options={ 
                {chart:{
                    title:"Expenses By Month"},
                    series: {
                      0: { axis: "Temps" },
                    },
                    axes: {
                      y: {
                        Temps: { label: "Amount" },
                      }
                    }
                  }
                }
              backgroundColor='white'/> 
          </Box>
        </main>

  )


}

export default dynamic(() => Promise.resolve(Home), { 
    ssr: false 
})
