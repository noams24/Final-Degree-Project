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
  const {userId,groupId} = JSON.parse(req.body)
 
  if(!groupId){
    return res.status(400).json({message:"Invalid group id"})
  }

  const userQuery = userId !== null ? `and fk_user_id ='${userId}'` : ''
  const filteredByCategories = await prisma.$queryRawUnsafe(`
  select cast(sum(amount) as int),category_name
  from userproducts 
  where fk_group_id='${groupId}'
  ${userQuery}
  group by category_name
  `) as UsersAndGroups[]

  
  
  const categoryAndAmountDic:any[] = [["category","amount"]]

  filteredByCategories.forEach((d)=>{
    const amount = d.sum;
    const category = d.category_name
    categoryAndAmountDic.push([category,amount])
  })
res.status(200).json({categoryAndAmountDic})
}
