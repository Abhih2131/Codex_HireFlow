'use client'
import Link from 'next/link'
const links = ['/employees','/admin/appusers','/requisitions','/approvals/inbox','/candidates','/pipeline','/admin/config','/communications/log','/audit']
export default function Nav(){
  return <nav className='flex gap-4 p-4 border-b bg-white text-sm'>{links.map(l=><Link key={l} href={l}>{l}</Link>)}</nav>
}
