class MessageManager {

    constructor() {

        this.conversations = new Map();

        this.inactivityTimers = new Map();

        this.MESSAGE_DELAY = 3000;

        this.REPLY_COOLDOWN = 2000;

    }

    // ======================================================
    // Crear conversación
    // ======================================================

    ensureConversation(key) {

        if (!this.conversations.has(key)) {

            this.conversations.set(key, {

                messages: [],

                timer: null,

                processing: false,

                lastReplyAt: 0,

                createdAt: new Date(),

                updatedAt: new Date(),

            });

        }

        return this.conversations.get(key);

    }

    // ======================================================
    // Agregar mensaje
    // ======================================================

    addMessage(key, message) {

        const conversation = this.ensureConversation(key);

        conversation.messages.push(message);

        conversation.updatedAt = new Date();

    }

    // ======================================================
    // Obtener mensajes
    // ======================================================

    getMessages(key) {

        const conversation = this.ensureConversation(key);

        return conversation.messages;

    }

    // ======================================================
    // Obtener texto completo
    // ======================================================

    getJoinedMessages(key) {

        const conversation = this.ensureConversation(key);

        return conversation.messages.join("\n");

    }

    // ======================================================
    // Limpiar mensajes
    // ======================================================

    clearMessages(key) {

        const conversation = this.ensureConversation(key);

        conversation.messages = [];

    }

    // ======================================================
    // Timer
    // ======================================================

    setTimer(key, timer) {

        const conversation = this.ensureConversation(key);

        if (conversation.timer) {

            clearTimeout(conversation.timer);

        }

        conversation.timer = timer;

    }

    clearTimer(key) {

        const conversation = this.ensureConversation(key);

        if (conversation.timer) {

            clearTimeout(conversation.timer);

        }

        conversation.timer = null;

    }
    // ======================================================
    // Timer de inactividad
    // ======================================================

    setInactivityTimer(key, timer) {

        if (this.inactivityTimers.has(key)) {

            clearTimeout(

                this.inactivityTimers.get(key)

            );

        }

        this.inactivityTimers.set(

            key,

            timer,

        );

    }

    clearInactivityTimer(key) {

        if (!this.inactivityTimers.has(key)) {

            return;

        }

        clearTimeout(

            this.inactivityTimers.get(key)

        );

        this.inactivityTimers.delete(key);

    }
    // ======================================================
    // Procesamiento
    // ======================================================

    isProcessing(key) {

        return this.ensureConversation(key).processing;

    }

    startProcessing(key) {

        this.ensureConversation(key).processing = true;

    }

    finishProcessing(key) {

        this.ensureConversation(key).processing = false;

    }

    // ======================================================
    // Cooldown
    // ======================================================

    canReply(key) {

        const conversation = this.ensureConversation(key);

        return (

            Date.now() - conversation.lastReplyAt

            >=

            this.REPLY_COOLDOWN

        );

    }

    markReply(key) {

        this.ensureConversation(key).lastReplyAt = Date.now();

    }

    // ======================================================
    // Eliminar conversación
    // ======================================================

    removeConversation(key) {

        const conversation = this.conversations.get(key);

        if (!conversation) {

            return;

        }

        if (conversation.timer) {

            clearTimeout(

                conversation.timer

            );

        }

        this.clearInactivityTimer(key);

        this.conversations.delete(key);

    }

    // ======================================================
    // Estadísticas
    // ======================================================

    count() {

        return this.conversations.size;

    }

    getAll() {

        return this.conversations;

    }

}

module.exports = new MessageManager();