<script lang="ts">
    import Map from "./Map.svelte";
</script>

<main>
    <div class="animated-bg"></div>
    <div class="circle circle1"></div>
    <div class="circle circle2"></div>
    <div class="circle circle3"></div>
    <header class="navbar is-primary">
        <div class="navbar-title">
            <strong>mapified</strong>
        </div>
        <div class="navbar-desc">
            <p>music. memory. place.</p>
        </div>
    </header>
    <div class="map-container">
        <Map />
    </div>

    <footer>
        <p><small>lovingly crafted in 2025 by sizhens</small></p>
    </footer>
</main>

<style>
    :global(html, body) {
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    :global(body) {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    main {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }

    header {
        flex: 0 0 auto;
        min-height: 5vh;
    }

    :global(.map-container) {
        flex: 1 1 auto;
        max-width: 1280px;
        overflow-x: hidden;
    }

    footer {
        flex: 0 0 auto;
    }
    .animated-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -2;
        background: linear-gradient(-45deg, #2f5249, #437057, #97b067);
        background-size: 400% 400%;
        animation: gradientMove 15s ease infinite;
    }

    @keyframes gradientMove {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    header {
        color: white;
        text-align: center;
        font-family:
            "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
            "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
        .navbar-title {
            padding-top: 10px;
            font-size: 150%;
            animation: float4 2.1s ease-in-out infinite alternate;
        }
        .navbar-desc {
            padding-bottom: 10px;
            animation: float4 2s ease-in-out infinite alternate;
        }
    }
    footer {
        color: white;
        text-align: center;
        font-size: 10px;
    }
    .circle {
        position: fixed;
        border-radius: 50%;
        opacity: 0.2;
        z-index: -1; /* above gradient, behind map UI */
    }

    /* Individual circles with unique positions and animations */
    .circle1 {
        width: 400px;
        height: 400px;
        background: forestgreen;
        top: 10%;
        left: 20%;
        animation: float1 9s ease-in-out infinite alternate;
    }

    .circle2 {
        width: 600px;
        height: 600px;
        background: forestgreen;
        top: 50%;
        left: 2%;
        animation: float2 13s ease-in-out infinite alternate;
    }

    .circle3 {
        width: 300px;
        height: 300px;
        background: forestgreen;
        top: 70%;
        left: 90%;
        animation: float3 18s ease-in-out infinite alternate;
    }

    /* Floating keyframes */
    @keyframes float1 {
        0% {
            transform: translateY(0) translateX(0);
        }
        100% {
            transform: translateY(-50px) translateX(100px);
        }
    }

    @keyframes float2 {
        0% {
            transform: translateY(0) translateX(0);
        }
        100% {
            transform: translateY(250px) translateX(-150px);
        }
    }

    @keyframes float3 {
        0% {
            transform: translateY(0) translateX(-50px);
        }
        100% {
            transform: translateY(-150px) translateX(50px);
        }
    }
    @keyframes float4 {
        0% {
            transform: translateY(0) translateX(0);
        }
        100% {
            transform: translateY(-10px) translateX(0px);
        }
    }
</style>
