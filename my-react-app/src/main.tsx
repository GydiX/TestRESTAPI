import {createRoot} from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import {GoogleOAuthProvider} from "@react-oauth/google";

createRoot(document.getElementById('root')!).render(
    <>
        <GoogleOAuthProvider clientId="383592103236-fh3qq91bulv9dsjse0agjb40eh3o82b0.apps.googleusercontent.com">
            <App/>
        </GoogleOAuthProvider>
    </>,
)
