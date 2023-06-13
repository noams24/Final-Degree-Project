import prisma from '@/lib/prisma'
import type { NextApiRequest, NextApiResponse } from 'next'

type UsersAndGroups = {
  sum: number,
  category_name: string,
  date_created:string,
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const {groupId,userId, dateFilter} = JSON.parse(req.body)
 
  if(!groupId){
    return res.status(400).json({message:"Invalid group id"})
  }

const dateQuery = dateFilter !== 'all'? `and up.date_created > CURRENT_DATE -${dateFilter}` :'' 
const userQuery = userId !== null ? `and fk_user_id ='${userId}'` : ''
const dbRes = (await  prisma.$queryRawUnsafe(`
    SELECT u.user_name, cast(sum(up.amount) as int)
    from userproducts up join users u on up.fk_user_id = u.pk_id
    where fk_group_id='${groupId}'
    ${userQuery}
    ${dateQuery}
    group by u.user_name
`)) as any[];

const userNameAndAmountDic:any[] = [["user name","amount"]]

let totalExpenses = 0;
dbRes.forEach((d)=>{
  const amount = d.sum;
  const userName = d.user_name
  totalExpenses+= amount;
  userNameAndAmountDic.push([userName,amount])
})

res.status(200).json({userNameAndAmountDic,totalExpenses})//,monthAndAmount})

}
