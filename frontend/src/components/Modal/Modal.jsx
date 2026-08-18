import "./Modal.css";

import { X } from "lucide-react";

function Modal({
    open,
    title,
    children,
    onClose,
    footer,
    className = "",
}) {

    if (!open) return null;

    return (

        <div className="modal-overlay">

            <div className={`modal ${className}`}>

                <div className="modal-header">

                    <h2>{title}</h2>

                    <button
                        className="modal-close"
                        onClick={onClose}
                        type="button"
                    >

                        <X size={22} />

                    </button>

                </div>

                <div className="modal-body">

                    {children}

                </div>

                {footer && (

                    <div className="modal-footer">

                        {footer}

                    </div>

                )}

            </div>

        </div>

    );
}

export default Modal;