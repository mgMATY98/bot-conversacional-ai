require("dotenv").config();

const express = require("express");

const sessionRoutes = require("./routes/session.routes");

const app = express();
const broadcastRoutes =
    require("./routes/broadcast.routes");
app.use(express.json());

app.use("/sessions", sessionRoutes);
app.use(
    "/broadcasts",
    broadcastRoutes
);
app.get("/", (req, res) => {

    res.json({
        service: "WhatsApp Gateway",
        status: "running",
        version: "1.0.0",
    });

});

const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {

    console.log("");
    console.log("====================================");
    console.log("🚀 WhatsApp Gateway iniciado");
    console.log(`Puerto : ${PORT}`);
    console.log("Esperando solicitudes...");
    console.log("====================================");

});