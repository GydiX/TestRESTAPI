// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import axios from 'axios'
import './App.css'
import { useEffect, useState } from 'react'
import {useGoogleLogin} from "@react-oauth/google";

function App() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    axios.get('http://localhost:8000/api/products/')
      .then(response => {
        setProducts(response.data)
        setLoading(false)
      })
      .catch(error => {
        setError(error.message)
        setLoading(false)
      })
  }, [])

  const loginByGoogle = useGoogleLogin({
    onSuccess: tokenResponse => {
      console.log("access_token", tokenResponse.access_token)
    },
  });

  return (
    <>
      <h1>Product List</h1>
      <button onClick={() => loginByGoogle()}>Sign in with Google 🚀</button>
      {loading && <p>Loading...</p>}
      {error && <p style={{color: 'red'}}>Error: {error}</p>}
      <div style={{display: 'flex', flexWrap: 'wrap', gap: '24px', marginTop: '24px'}}>
        {products.map((product) => (
          <div key={product.id} style={{border: '1px solid #ccc', borderRadius: '8px', padding: '16px', width: '260px'}}>
            {product.images && product.images.length > 0 && (
              <img src={product.images[0].image} alt={product.images[0].alt_text || product.name} style={{width: '100%', height: '180px', objectFit: 'cover', borderRadius: '4px'}} />
            )}
            <h2 style={{margin: '12px 0 4px 0'}}>{product.name}</h2>
            <p style={{margin: '0 0 8px 0', color: '#555'}}>{product.category?.name}</p>
            <p style={{fontWeight: 'bold', margin: 0}}>{product.price} ₴</p>
            <p style={{fontSize: '0.95em', color: '#888', marginTop: '8px'}}>{product.description}</p>
          </div>
        ))}
      </div>
    </>
  )
}

export default App
