'use client'
import { useState } from 'react'
import { api } from '@/lib/api'
export default function Login(){
  const [identifier,setId]=useState('admin@workplaceai.local'); const [code,setCode]=useState('123456'); const [msg,setMsg]=useState('')
  return <div className='space-y-2 max-w-md'><h1 className='text-xl'>Login OTP</h1>
    <input className='border p-2 w-full' value={identifier} onChange={e=>setId(e.target.value)} placeholder='email'/>
    <button className='bg-black text-white px-3 py-2' onClick={async()=>{const r=await api('/auth/otp/request',{method:'POST',body:JSON.stringify({identifier})}); setMsg(`DEV OTP: ${r.dev_otp}`)}}>Request OTP</button>
    <input className='border p-2 w-full' value={code} onChange={e=>setCode(e.target.value)} placeholder='otp'/>
    <button className='bg-blue-600 text-white px-3 py-2' onClick={async()=>{const r=await api('/auth/otp/verify',{method:'POST',body:JSON.stringify({identifier,code})}); localStorage.setItem('token',r.access_token); setMsg('Logged in')}}>Verify</button>
    <div>{msg}</div>
  </div>
}
