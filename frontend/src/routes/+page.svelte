<script>
  import { onMount } from 'svelte';
  import FormularioMovimiento from '$lib/FormularioMovimiento.svelte';
  import ListaMovimientos from '$lib/ListaMovimientos.svelte';
  import DashboardGraficos from '$lib/DashboardGraficos.svelte';
  import Facturacion from '$lib/Facturacion.svelte';
  import ExportarMovimientos from '$lib/ExportarMovimientos.svelte';
  import ExportarFacturacion from '$lib/ExportarFacturacion.svelte';
  import AuthGate from '$lib/AuthGate.svelte';
  import { PUBLIC_API_URL } from '$env/static/public';

  const API = {PUBLIC_API_URL}


  console.log("PUBLIC_API_URL:", PUBLIC_API_URL)


  let movimientos = [];
  let tab = "ingresos";
  let busqueda = "";

  async function cargarMovimientos() {
    const res = await fetch(`${API}/movimientos`);
    movimientos = await res.json();
  }

  async function agregarMovimiento(data) {
    const res = await fetch(`${API}/movimientos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (res.ok) {
      await cargarMovimientos();
    } else {
      const errorText = await res.text();
      console.error("Error al agregar:", res.status, errorText);
    }
  }

  async function eliminarMovimiento(id) {
    const res = await fetch(`${API}/movimientos/${id}`, {
      method: "DELETE"
    });
    if (res.ok) await cargarMovimientos();
  }

  onMount(cargarMovimientos);
</script>

<AuthGate claveCorrecta ="titibaradero">
<div class="min-h-screen w-full bg-gradient-to-b from-pink-200 via-pink-100 to-white text-gray-800 font-sans px-4 py-6">
  <h1 class="text-5xl sm:text-6xl font-extrabold text-center tracking-widest text-gray-900 relative mb-10 font-sans">
    <span class="relative z-10 drop-shadow-md">TITICASH</span>
    <span class="absolute left-1/2 bottom-0 w-2/3 h-1 bg-gradient-to-r from-pink-400 to-fuchsia-500 -translate-x-1/2 rounded-full z-0"></span>
  </h1>

  <div class="flex justify-center gap-6 mb-8 flex-wrap">
    <button on:click={() => tab = "ingresos"} class="px-4 py-1 border-b-2 transition-all duration-200" class:selected={tab === 'ingresos'}>INGRESOS</button>
    <button on:click={() => tab = "egresos"} class="px-4 py-1 border-b-2 transition-all duration-200" class:selected={tab === 'egresos'}>EGRESOS</button>
    <button on:click={() => tab = "movimientos"} class="px-4 py-1 border-b-2 transition-all duration-200" class:selected={tab === 'movimientos'}>MOVIMIENTOS</button>
  </div>

  <div class="max-w-screen-2xl mx-auto grid grid-cols-1 lg:grid-cols-4 gap-6">
    <div class="hidden lg:block">
      <DashboardGraficos {movimientos} />
    </div>

    <div class="lg:col-span-2">
      {#if tab === "movimientos"}
        <ExportarMovimientos {movimientos} />
        <div class="mb-4">
          <input
            type="text"
            placeholder="Buscar por descripción, categoría o monto"
            bind:value={busqueda}
            class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-400 text-sm"
          />
        </div>
        <ListaMovimientos tipo="todos" {movimientos} filtro={busqueda} onEliminar={eliminarMovimiento} />
      {:else}
        <FormularioMovimiento {tab} tipo={tab} onAgregar={agregarMovimiento} />
        <ListaMovimientos tipo={tab} {movimientos} onEliminar={eliminarMovimiento} />
      {/if}
    </div>

    <div>
      <Facturacion {movimientos} />
      
    </div>
  </div>
</div>
</AuthGate>

<style>
  button.selected {
    border-color: black;
    font-weight: bold;
  }
</style>
