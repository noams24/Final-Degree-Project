import { Inter } from 'next/font/google'
import { clearFromSession, getFromStorage } from '@/lib/session-storage'
import React from 'react'
import { User } from '@/types/user'
import { useRouter } from 'next/router'
import dynamic from 'next/dynamic';
import PieChart from '@/components/pie-chart'


type ServerUsersAndGroups = {
  groupName: string,
  groupId: number,
  users: { id: number, name: string }[]
}

type ProductsResponse = {
  categoryAndAmountDic: any
}
const inter = Inter({ subsets: ['latin'] })

const Home = function (props: any) {

  const user = getFromStorage('user') as User
  const [groups, setGroups] = React.useState<ServerUsersAndGroups[]>([])
  const [selectedGroup, setSelectedGroup] = React.useState<any>(null)
  const [selectedUser, setSelectedUser] = React.useState<any>(null)
  const [dataByCategories, setDataByCategories] = React.useState<(string | number)[][]>([])
  const router = useRouter()
  const onLogout = function () {
    router.push("/login")
    clearFromSession('user')
  }
  const getUserGroups = async function () {
    // Get data from server
    const res = await fetch("/api/user-data", {
      method: "POST",
      body: JSON.stringify({
        userId: user.pk_id,
      })
    })
    const data = await res.json()
    setGroups(data.usersGroupsMap)
    setSelectedGroup(Object.keys(data.usersGroupsMap)[0])
    setSelectedUser("all")
  }


  const getProducts = async function (userId: string, groupId: string) {
    const res = await fetch("/api/expenses", {
      method: "POST",
      body: JSON.stringify({
        userId: userId === "all" ? null : userId,
        groupId
      })
    })
    const data = await res.json() as ProductsResponse
    const { categoryAndAmountDic } = data
    setDataByCategories(categoryAndAmountDic)
  }
  const onGroupSelect = function (e: React.ChangeEvent<HTMLSelectElement>) {
    const groupId = e.target.value;
    setSelectedGroup(groupId)
    setSelectedUser("all")
  };

  const onUserSelect = function (e: React.ChangeEvent<HTMLSelectElement>) {
    const userId = e.target.value;
    setSelectedUser(userId)
  };

  React.useEffect(() => {
    if (!user) {
      router.push("/login")
      return
    }
    getUserGroups()
  }, [])

  React.useEffect(() => {
    if (selectedGroup === null) return
    getProducts(selectedUser, selectedGroup)
  }, [selectedGroup, selectedUser])

  if (!user) {
    return <div>Loading..</div>
  }
  //console.log(user)
  const optionss = {
    title: "Categories", backgroundColor: "white", titleTextStyle: { color: 'black' },
    legend: { textStyle: { color: 'black' } }
  }


  return (
    <>
      <main className={inter.className}>
        <header className="container max-w-2xl px-6 py-14 mx-auto">
          <div className="flex items-center justify-between">
            <div className="font-bold">
            <h1>Hello   <span>{user?.user_name || ""} </span> </h1>
            </div>
            <div>
              <button className="btn btn-danger" onClick={onLogout}>Sign out</button>
            </div>
          </div>
          <div className="flex pt-8">
            <h1>Group</h1>
            <div className='px-6'>
              <h1>User</h1>
            </div>
          </div>
          {/*Show Groups  */}
          <div className='flex items-center text-black'>

            <select defaultValue={groups[selectedGroup]?.groupName} onChange={onGroupSelect}>
              {Object.values(groups)?.map((gr) => <option key={gr.groupId} value={gr.groupId}>{gr.groupName}</option>)}
            </select>

            {/* Show Users */}
            <div className='px-3'>

              <select value={selectedUser} defaultValue={selectedUser} onChange={onUserSelect}>
                <option value="all">All</option>
                {groups[selectedGroup]?.users?.map((user) => <option key={user.id} value={user.id}>{user.name}</option>)}
              </select>
            </div>
          </div>

          {/* Pie chart */}
          <div className='flex bg-white shadow-md rounded-lg px-15 mt-10'>
            {dataByCategories?.length > 0 ? <PieChart data={dataByCategories} options={optionss} /> : null}
          </div>
        </header>
      </main>
    </>
  )
}



export default dynamic(() => Promise.resolve(Home), {
  ssr: false
})