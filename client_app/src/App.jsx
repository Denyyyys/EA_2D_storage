import { useState } from 'react'
import './styles/index.css';
import Navbar from './components/navbar';
import StoreForm from './components/storeForm';
import ShapesList from './components/ShapesList';
import Result from './components/Result';


function App() {

  return (
    <>
      <Navbar />
      <div className="main-container">
        <StoreForm />
        <ShapesList />
      </div>
      <div className=' result-container cont'>
        <Result />
      </div>
    </>
  )
}

export default App
