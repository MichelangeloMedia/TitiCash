<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  export let claveCorrecta = "titibaradero";

  let claveIngresada = "";
  let autenticado = false;

  onMount(() => {
    if (browser) {
      const guardada = localStorage.getItem("clave");
      if (guardada === claveCorrecta) {
        autenticado = true;
      }
    }
  });

  function verificarClave() {
    if (claveIngresada === claveCorrecta) {
      autenticado = true;
      if (browser) {
        localStorage.setItem("clave", claveCorrecta);
      }
    } else {
      alert("Clave incorrecta");
    }
  }
</script>

{#if autenticado}
  <slot />
{:else}
  <div class="min-h-screen flex items-center justify-center bg-pink-100 text-center p-4">
    <div class="bg-white rounded-xl shadow-lg p-6 max-w-sm w-full space-y-4">
      <h2 class="text-lg font-semibold text-gray-800">Acceso restringido</h2>
      <input
        type="password"
        bind:value={claveIngresada}
        class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-pink-400"
        placeholder="Ingresá la clave"
        on:keydown={(e) => e.key === 'Enter' && verificarClave()}
      />
      <button
        on:click={verificarClave}
        class="w-full bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600 transition"
      >
        Ingresar
      </button>
    </div>
  </div>
{/if}