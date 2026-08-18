import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import AdminPage from "./pages/AdminPage";

import ProtectedRoute from "./components/ProtectedRoute";

import ClientLayout from "./layouts/ClientLayout/ClientLayout";

import ClientDashboard from "./components/Client/Dashboard/ClientDashboard";
import AI from "./components/Client/AI/AI";
import Documents from "./components/Client/Documents/Documents";
import Conversations from "./components/Client/Conversations/Conversations";
import WhatsApp from "./components/Client/WhatsApp/WhatsApp";
import Ideas from "./components/Client/Ideas/Ideas";
import Settings from "./components/Client/Settings/Settings";
import BehaviorSection from "./components/Client/Behavior/Behavior";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                {/* LOGIN */}

                <Route

                    path="/"

                    element={<LoginPage />}

                />

                {/* ADMIN */}

                <Route

                    path="/admin"

                    element={

                        <ProtectedRoute allowedRole="admin">

                            <AdminPage />

                        </ProtectedRoute>

                    }

                />

                {/* CLIENTE */}

                <Route

                    path="/client"

                    element={

                        <ProtectedRoute allowedRole="client">

                            <ClientLayout />

                        </ProtectedRoute>

                    }

                >

                    <Route

                        index

                        element={<ClientDashboard />}

                    />

                    <Route

                        path="dashboard"

                        element={<ClientDashboard />}

                    />

                    <Route

                        path="ai"

                        element={<AI />}

                    />
                    <Route
                        path="behavior"
                        element={<BehaviorSection />}
                    />

                    <Route

                        path="documents"

                        element={<Documents />}

                    />

                    <Route

                        path="conversations"

                        element={<Conversations />}

                    />

                    <Route

                        path="whatsapp"

                        element={<WhatsApp />}

                    />

                    <Route

                        path="ideas"

                        element={<Ideas />}

                    />

                    <Route

                        path="settings"

                        element={<Settings />}

                    />

                </Route>

            </Routes>

        </BrowserRouter>

    );

}

export default App;