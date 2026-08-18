import "./BehaviorCard.css";

function BehaviorCard({

    icon: Icon,

    title,

    children,

}) {

    return (

        <div className="behavior-card">

            <div className="behavior-card-header">

                <Icon size={22} />

                <h2>{title}</h2>

            </div>

            <div className="behavior-form">

                {children}

            </div>

        </div>

    );

}

export default BehaviorCard;