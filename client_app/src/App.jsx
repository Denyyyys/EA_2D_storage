import { useState } from 'react'
import './styles/index.css';
import Navbar from './components/navbar'
import StoreForm from './components/StoreForm'
import ShapesList from './components/ShapesList';


function App() {

  return (
    <>
      <Navbar />
      <div className="main-container">
        <StoreForm />
        <ShapesList />
      </div>
    </>
  )
}

export default App
