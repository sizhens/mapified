<script lang="ts">
    import { onMount } from "svelte";
    import L, { LatLng, Map as LeafletMap } from "leaflet";
    import "leaflet/dist/leaflet.css";
    import PinForm from "./PinForm.svelte";
    import type { Pin } from "../types";
    import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
    import iconUrl from "leaflet/dist/images/marker-icon.png";
    import shadowUrl from "leaflet/dist/images/marker-shadow.png";

    delete L.Icon.Default.prototype._getIconUrl;

    L.Icon.Default.mergeOptions({
        iconRetinaUrl,
        iconUrl,
        shadowUrl,
    });

    let map: LeafletMap;
    let pins: Pin[] = [];
    let newPinCoords: { lat: number; lng: number } | null = null;
    let popup: L.Popup | null = null;
    let pinFormPosition: { x: number; y: number } | null = null;

    const BACKENDURL = "https://mapified.onrender.com/pins";

    function makeSpotifyEmbedURL(url: string) {
        if (!url) return "";
        return url.replace("open.spotify.com/", "open.spotify.com/embed/");
    }

    function stripSpotifyParams(url: string) {
        return url.split("?")[0];
    }

    async function fetchPins() {
        try {
            const res = await fetch(BACKENDURL);
            const pins: Pin[] = await res.json();

            pins.forEach((pin) => {
                addPin(pin);
            });
        } catch (err) {
            console.error("Error fetching pins:", err);
        }
    }

    function addPin(pin: Pin) {
        pins.push(pin);
        const marker = L.marker([pin.lat, pin.lng]).addTo(map);

        let popupHTML = "";
        popupHTML += `<iframe src="${makeSpotifyEmbedURL(stripSpotifyParams(pin.spotify_url))}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>`;
        if (pin.text) {
            popupHTML += `<p>${pin.text}</p>`;
        }
        if (pin.created_at) {
            popupHTML += `<small>${new Date(pin.created_at).toLocaleString()}-UTC</small>`;
        }
        marker.bindPopup(popupHTML).openPopup();
    }
    function handleAddPin(pin: Pin) {
        addPin(pin);
        if (popup) map.closePopup(popup);
    }

    onMount(() => {
        map = L.map("map").setView([39.95, -75.15], 13);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);
        fetchPins();
        map.on("click", (e) => {
            if (popup) map.closePopup(popup);
            newPinCoords = { lat: e.latlng.lat, lng: e.latlng.lng };
            const pointx = e.originalEvent.clientX;
            const pointy = e.originalEvent.clientY;
            pinFormPosition = { x: pointx, y: pointy };
        });
    });
</script>

<main>
    <div id="map"></div>
    {#if newPinCoords}
        {#if pinFormPosition}
            <div
                class="pin-form-wrapper"
                style="position:absolute;
                width:220px;
                height:300px;
                left:{pinFormPosition.x - 115}px;
                top:{pinFormPosition.y - 130}px; z-index:1000;"
            >
                <PinForm
                    lat={newPinCoords.lat}
                    lng={newPinCoords.lng}
                    onAddPin={(pin) => {
                        addPin(pin);
                        newPinCoords = null;
                    }}
                    onCancel={() => {
                        newPinCoords = null;
                    }}
                />
            </div>
        {/if}
    {/if}
</main>

<style>
    #map {
        height: 80vh;
        width: 80vw;
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        position: relative;
    }
</style>
