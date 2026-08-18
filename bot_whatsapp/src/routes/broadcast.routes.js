const express = require("express");

const broadcastController =
    require("../controllers/broadcast.controller");


const router =
    express.Router();


router.post(
    "/start",
    (req, res) =>
        broadcastController.start(
            req,
            res
        )
);


module.exports = router;