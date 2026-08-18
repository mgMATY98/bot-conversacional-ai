const express = require("express");

const controller = require("../controllers/session.controller");

const router = express.Router();


// ==========================================================
// DESCONECTAR
// ==========================================================

router.post(
    "/:id/disconnect",
    controller.disconnect
);


// ==========================================================
// RECONECTAR
// ==========================================================

router.post(
    "/:id/reconnect",
    controller.reconnect
);


// ==========================================================
// OBTENER SESIÓN
// ==========================================================

router.get(
    "/:id",
    controller.get
);


// ==========================================================
// OBTENER QR
// ==========================================================

router.get(
    "/:id/qr",
    controller.getQR
);


// ==========================================================
// ENVIAR MENSAJE
// ==========================================================

router.post(
    "/:id/message",
    controller.sendMessage
);


// ==========================================================
// CREAR SESIÓN
// ==========================================================

router.post(
    "/",
    controller.create
);


module.exports = router;