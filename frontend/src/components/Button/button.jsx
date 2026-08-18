import "./Button.css";

function Button({

    children,

    onClick,

    type = "button",

    disabled = false,

    variant = "primary",

    size = "md",

    fullWidth = false

}) {

    return (

        <button

            type={type}

            disabled={disabled}

            onClick={onClick}

            className={`
                btn
                btn-${variant}
                btn-${size}
                ${fullWidth ? "btn-full" : ""}
            `}

        >

            {children}

        </button>

    );

}

export default Button;