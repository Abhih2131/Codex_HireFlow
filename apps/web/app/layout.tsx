import './globals.css'
import Nav from '@/components/Nav'
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html><body><div className='font-semibold p-4'>WorkplaceAI HireFlow — Configure workflows. Not code.</div><Nav /><main className='p-4'>{children}</main></body></html>
}
