import bcrypt from 'bcryptjs';
import prisma from '@/lib/prisma'
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { login_name,password} = JSON.parse(req.body)
  
  if(!login_name){
    return res.status(404).json({message:"No login name provided"});
  
  }

  // Try to find the user
  const user = await prisma.users.findFirst({
    where:{
    login_name:(login_name as string).toLowerCase(),
    }
  })
  
  if(!user){
    return  res.status(404).json({message:"User not found"});
  }

  // Try to find the hashed password
  const storedHashedPassword:any = await prisma.$queryRawUnsafe(`
    select password
    from users 
    where login_name='${login_name}'
  `) as any[];
  // compare it to the input password
  const match: any =bcrypt.compareSync(password, storedHashedPassword[0].password);
  if(!match){
    return  res.status(404).json({message:"Password incorrect"});
  }
  
  return res.status(200).json(user)
}

