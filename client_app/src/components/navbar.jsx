import logo from '../assets/logo.svg';
const Navbar = () => {
  return (
    <div className="navbar">
      <div className="logo">
        <img src={logo} alt="logo" className='logo-img' />
      </div>
      <div className="nav-links">
        <a href="https://github.com/Denyyyys/EA_2D_storage" target='_blank'>About Project</a>
      </div>
    </div>
  )
}


export default Navbar;