'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
export default function Reqs(){
  const [rows,setRows]=useState<any[]>([]); const [title,setTitle]=useState('Software Engineer');
  const load=()=>api('/requisitions').then(setRows)
  useEffect(()=>{load()},[])
  return <div><h1 className='text-xl'>Requisitions</h1><button className='bg-black text-white px-2 py-1' onClick={async()=>{await api('/requisitions',{method:'POST',body:JSON.stringify({title,hm_employee_id:'E0001',headcount:1})});load()}}>Create</button>
  <pre className='bg-white border p-3 text-xs mt-3'>{JSON.stringify(rows,null,2)}</pre></div>
}
