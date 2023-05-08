import ExpenseComponent from "../../components/ExpenseComponent";
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

const Home2 = function (props: any) {

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
    console.log(categoryAndAmountDic)

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
}


const DUMMY_DATA = [
  {
    id: 1,
    title: "Entertainment",
    color: "#FF33FF",
    total: 500,
  },
  {
    id: 2,
    title: "Rent",
    color: "#009",
    total: 200,
  },
  {
    id: 3,
    title: "Fuel",
    color: "#000",
    total: 1200,
  },
  {
    id: 4,
    title: "Movies",
    color: "#532",
    total: 800,
  },
  {
    id: 5,
    title: "Holiday",
    color: "#66FFFF",
    total: 2000,
  },
];


export default function Home() {
  return (
    <>
      <main className="container max-w-2xl px-6 mx-auto">
        {/* Expenses */}
        <section className="py-6">
          <h3 className="text-2xl">Latest Expenses</h3>
          <div className="flex flex-col gap-4 mt-6">
            {DUMMY_DATA.map((expense) => {
              return (
                <ExpenseComponent
                  color={expense.color}
                  title={expense.title}
                  total={expense.total}
                />
              );
            })}
          </div>
        </section>
      </main>
    </>
  );
}

