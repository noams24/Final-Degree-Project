import prisma from '@/lib/prisma'
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const {groupId,userId} = JSON.parse(req.body)
 
  if(!groupId){
    return res.status(400).json({message:"Invalid group id"})
  }

//const dateQuery = dateFilter !== 'all'? `and up.date_created > CURRENT_DATE -${dateFilter}` :'' 
const userQuery = userId !== null ? `and fk_user_id ='${userId}'` : ''
const dbRes = (await  prisma.$queryRawUnsafe(`
    SELECT u.user_name, cast(sum(up.amount) as int), EXTRACT(MONTH FROM up.date_created) AS month
    from userproducts up join users u on up.fk_user_id = u.pk_id
    where fk_group_id='${groupId}'
    ${userQuery}
    group by u.user_name, month
`)) as any[];

const monthAndAmount:any[] = [["month","amount"],[1,],[2,],[3,],[4,],[5,],[6,],[7,],[8,],[9,],[10,],[11,],[12,]]

let totalExpenses = 0;
dbRes.forEach((d)=>{
  const amount = d.sum;
  const month = d.month;
  const currentAmount = monthAndAmount[month][1];
  const hasValue = currentAmount !== undefined;
  if(hasValue) {
    monthAndAmount[month][1] = currentAmount + amount;
  }
  else{
    monthAndAmount[month].push(amount)
  }
  
})

//in case the month has no expenses add 0 to array for data display
for(let i = 0; i < monthAndAmount.length; i++){
  if(monthAndAmount[i].length < 2){
    monthAndAmount[i].push(0);
  }
}

res.status(200).json({monthAndAmount})

}
