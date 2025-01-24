/*
* Based in https://glitch.com/edit/#!/whatsapp-cloud-api-echo-bot
* Copyright (c) Meta Platforms, Inc. and affiliates, licensed under the MIT license.
*/

// Debe ejecutar el siguiente comando en la terminal del servidor Glitch:
// You must run the following command in the Glitch server terminal:
// npm install async-mutex

import express from "express";
import axios from "axios";
import { Mutex } from "async-mutex";

const app = express();
app.use(express.json());

const { WEBHOOK_VERIFY_TOKEN, GRAPH_API_TOKEN, PORT } = process.env;

let unprocessedMessages = [];
const mutex = new Mutex();

app.post("/webhook", async (req, res) => {
    console.log("Incoming webhook message:", JSON.stringify(req.body, null, 2));

    const message = req.body.entry?.[0]?.changes[0]?.value?.messages?.[0];

    if (message?.type === "text") {
        // Use the mutex to ensure thread-safe access to the unprocessedMessages array
        await mutex.runExclusive(() => {
            unprocessedMessages.push(message);
            console.log("Message added to unprocessed messages list:", message);
        });

        // Extract the business number to send the reply from it
        const business_phone_number_id = req.body.entry?.[0].changes?.[0].value?.metadata?.phone_number_id;

        // Mark incoming message as read
        try {
            await axios({
                method: "POST",
                url: `https://graph.facebook.com/v18.0/${business_phone_number_id}/messages`,
                headers: {
                    Authorization: `Bearer ${GRAPH_API_TOKEN}`,
                },
                data: {
                    messaging_product: "whatsapp",
                    status: "read",
                    message_id: message.id,
                },
            });
        } catch (error) {
            console.error("Error marking message as read:", error);
        }
    }

    res.sendStatus(200);
});

app.get("/webhook", (req, res) => {
    const mode = req.query["hub.mode"];
    const token = req.query["hub.verify_token"];
    const challenge = req.query["hub.challenge"];

    if (mode === "subscribe" && token === WEBHOOK_VERIFY_TOKEN) {
        res.status(200).send(challenge);
        console.log("Webhook verified successfully!");
    } else {
        res.sendStatus(403);
    }
});

app.get("/", (req, res) => {
    res.send(`<pre>Nothing to see here. Checkout README.md to start.</pre>`);
});

app.listen(PORT, () => {
    console.log(`Server is listening on port: ${PORT}`);
});

app.get("/messages", async (req, res) => {
    // Use the mutex to ensure thread-safe access to the unprocessedMessages array
    const messages = await mutex.runExclusive(() => {
        const messagesCopy = [...unprocessedMessages];
        unprocessedMessages.length = 0; // Clear the array after copying
        return messagesCopy;
    });

    res.json(messages);
});
