'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export default function SimpleListPage({title, endpoint}:{title:string, endpoint:string}){
  const [rows,setRows]=useState<any[]>([])
  useEffect(()=>{api(endpoint).then(setRows).catch(()=>setRows([]))},[endpoint])
  return <div><h1 className='text-xl mb-3'>{title}</h1><pre className='bg-white border p-3 text-xs overflow-auto'>{JSON.stringify(rows,null,2)}</pre></div>
}
