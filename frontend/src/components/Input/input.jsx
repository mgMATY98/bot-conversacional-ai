import "./Input.css";

function Input({

    label,
    type = "text",
    value,
    onChange,
    placeholder,
    disabled = false,
    required = false,
    error = "",
    helperText = "",
    icon: Icon,
    rightIcon = null,
    fullWidth = true,
    ...props

}) {

    return (

        <div className={`input-group ${fullWidth ? "full" : ""}`}>

            {label && (

                <label className="input-label">

                    {label}

                    {required && (

                        <span className="required">

                            *

                        </span>

                    )}

                </label>

            )}

            <div className={`input-wrapper ${error ? "error" : ""}`}>

                {Icon && (

                    <Icon

                        size={18}

                        className="input-icon"

                    />

                )}

                <input

                    type={type}

                    value={value}

                    onChange={onChange}

                    placeholder={placeholder}

                    disabled={disabled}

                    {...props}

                />

                {rightIcon && (

                    <div className="input-right-icon">

                        {rightIcon}

                    </div>

                )}

            </div>

            {error ? (

                <span className="input-error">

                    {error}

                </span>

            ) : helperText ? (

                <span className="input-helper">

                    {helperText}

                </span>

            ) : null}

        </div>

    );

}

export default Input;