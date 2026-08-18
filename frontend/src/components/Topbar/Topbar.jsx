import "./Topbar.css";

function Topbar({ title }) {

    return (

        <header className="topbar">

            <h2>

                {title}

            </h2>

            <div className="topbar-user">

                🟢 Conectado

            </div>

        </header>

    );

}

export default Topbar;