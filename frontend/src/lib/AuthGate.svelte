<script>
  export let claveCorrecta = "juanabaradero";
  let claveIngresada = "";
  let autorizado = localStorage.getItem("autorizado") === "sí";

  function validar() {
    if (claveIngresada === claveCorrecta) {
      localStorage.setItem("autorizado", "sí");
      autorizado = true;
    } else {
      alert("Clave incorrecta");
    }
  }
</script>

{#if autorizado}
  <slot />
{:else}
  <div class="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-pink-200 to-fuchsia-300 p-4">
    <h1 class="text-3xl font-bold mb-6">🔐 Acceso restringido</h1>
    <input
      type="password"
      placeholder="Ingresá la clave"
      bind:value={claveIngresada}
      class="p-2 border border-gray-300 rounded mb-4 w-64 text-center"
    />
    <button
      on:click={validar}
      class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800"
    >
      Ingresar
    </button>
  </div>
{/if}