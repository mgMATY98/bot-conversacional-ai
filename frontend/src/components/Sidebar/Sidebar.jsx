import "./Sidebar.css";

function Sidebar({ menu }) {

    return (

        <aside className="sidebar">

            <div className="sidebar-logo">

                BotConversacional

            </div>

            <nav>

                {menu.map(item => (

                    <button
                        key={item.label}
                        className="sidebar-item"
                        onClick={item.onClick}
                    >

                        <span className="sidebar-icon">

                            {item.icon}

                        </span>

                        {item.label}

                    </button>

                ))}

            </nav>

        </aside>

    );

}

export default Sidebar;