import { mount } from "svelte";
import "./app.css";
import App from "./App.svelte";
const target = document.getElementById("app") as HTMLElement;

const app = mount(App, { target: document.getElementById("app")! });

export default app;
