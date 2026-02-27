'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
export default function AppUsers(){
  const [rows,setRows]=useState<any[]>([]); const [form,setForm]=useState<any>({employee_id:'E0001',email:'admin@workplaceai.local',role:'Super Admin',is_active:true})
  const load=()=>api('/admin/appusers').then(setRows)
  useEffect(()=>{load()},[])
  return <div><h1 className='text-xl'>AppUsers</h1>
  <textarea className='border w-full h-24' value={JSON.stringify(form)} onChange={e=>setForm(JSON.parse(e.target.value||'{}'))}/>
  <button className='bg-black text-white px-3 py-1' onClick={async()=>{await api('/admin/appusers',{method:'POST',body:JSON.stringify(form)});load()}}>Save</button>
  <pre className='bg-white border p-3 text-xs mt-3'>{JSON.stringify(rows,null,2)}</pre></div>
}
