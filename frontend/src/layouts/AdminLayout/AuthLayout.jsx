import "./AuthLayout.css";

function AuthLayout({ children }) {

    return (

        <div className="auth-page">

            <div className="auth-left">

                <h1>Bot Conversacional</h1>

                <p>
                    Plataforma inteligente para atención
                    automática por WhatsApp.
                </p>

            </div>

            <div className="auth-right">

                {children}

            </div>

        </div>

    );

}

export default AuthLayout;