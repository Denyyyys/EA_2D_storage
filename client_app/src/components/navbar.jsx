import logo from '../assets/vite.svg';
const Navbar = () => {
  return (
    <div className="navbar">
      <div className="logo">
        <img src={logo} alt="logo" />
      </div>
      <div className="nav-links">
        <a href="#">About Project</a>
      </div>
    </div>
  )
}


export default Navbar;