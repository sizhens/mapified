<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type { Pin } from "../types";

    export let lat: number = 0;
    export let lng: number = 0;

    export let onAddPin: (pin: Pin) => void;
    export let onCancel: () => void;
    let isSubmitting = false;

    export let spotifyURL = "";
    export let text = "";
    const BACKENDURL = "http://127.0.0.1:5000/pins";

    async function submit() {
        if (!spotifyURL) return alert("Spotify URL required");

        const newPin: Pin = {
            lat,
            lng,
            spotify_url: spotifyURL,
            text,
            created_at: new Date().toISOString(),
        };
        try {
            isSubmitting = true;
            const res = await fetch(BACKENDURL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newPin),
            });

            if (!res.ok) {
                const text = await res.text();
                throw new Error(`Failed to add pin: ${res.status} ${text}`);
            }

            onAddPin(newPin);
            onCancel();
        } catch (err) {
            console.error(err);
            alert("There was an error adding your pin. Please try again.");
        } finally {
            isSubmitting = false;
        }
    }
</script>

<main>
    <div class="pin-form">
        <input bind:value={spotifyURL} placeholder="Spotify URL (required)" />
        <textarea
            maxlength="1000"
            bind:value={text}
            placeholder="Leave a message! 💚"
        ></textarea>
        <div class="buttons">
            <button on:click={submit} disabled={isSubmitting}>
                {isSubmitting ? "Adding..." : "Add Pin"}
            </button>
            <button on:click={onCancel} disabled={isSubmitting}>Cancel</button>
        </div>
    </div>
</main>

<style>
    .pin-form {
        position: absolute;
        background: white;
        left: 30px;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        width: 220px;
        z-index: 1000;
    }
    .pin-form textarea {
        resize: none;
        width: 100%;
        height: 35px;
        box-sizing: border-box;
    }
    .pin-form::after {
        content: "";
        position: absolute;
        bottom: -10px;
        transform: translateX(-50%);
        border-width: 10px 8px 0 8px;
        border-style: solid;
        border-color: white transparent transparent transparent;
    }

    .buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.25rem;
    }
</style>
