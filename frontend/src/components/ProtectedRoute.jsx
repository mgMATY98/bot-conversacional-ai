import { Navigate } from "react-router-dom";

import { getToken } from "../utils/token";

function ProtectedRoute({

    children,
    allowedRole

}) {

    const token = getToken();

    const role = localStorage.getItem("role");

    if (!token) {

        return <Navigate to="/" replace />;

    }

    if (allowedRole && role !== allowedRole) {

        return <Navigate to="/" replace />;

    }

    return children;

}

export default ProtectedRoute;