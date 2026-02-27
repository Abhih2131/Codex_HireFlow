'use client'
import { useEffect, useState } from 'react'
import { API_URL, api } from '@/lib/api'
export default function Employees(){
  const [rows,setRows]=useState<any[]>([]); const [file,setFile]=useState<File|null>(null)
  const load=()=>api('/employees').then(setRows)
  useEffect(()=>{load()},[])
  return <div><h1 className='text-xl'>Employees</h1>
    <input type='file' onChange={e=>setFile(e.target.files?.[0]||null)} />
    <button className='bg-black text-white px-3 py-1 ml-2' onClick={async()=>{if(!file) return; const fd=new FormData(); fd.append('file',file); const t=localStorage.getItem('token'); await fetch(`${API_URL}/employees/import`,{method:'POST',headers:{Authorization:`Bearer ${t||''}`},body:fd}); load()}}>Import Now</button>
    <pre className='bg-white border p-3 text-xs mt-3'>{JSON.stringify(rows,null,2)}</pre></div>
}
