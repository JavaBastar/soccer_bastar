

async function load() {
    const container = document.getElementById("app");

    try {
        const res = await fetch("https://raw.githubusercontent.com/JavaBastar/soccer_bastar/main/backend/partidos.json");
        const data = await res.json();

        console.log("DATA:", data);

        localStorage.setItem("partidos_cache", JSON.stringify(data));

        const now = new Date();

        const fecha = now.toLocaleDateString("es-MX", {
            day: "2-digit",
            month: "2-digit"
        });

        const hora = now.toLocaleTimeString("es-MX", {
            hour: "2-digit",
            minute: "2-digit",
            hour12: false
        });

        localStorage.setItem("last_update", `Actualizado ${fecha} - ${hora}`);



        if (data.length === 0) {
            const last = localStorage.getItem("last_update");

            if (last) {
                document.getElementById("status").innerText = `🟡 Sin partidos • ${last}`;
            } else {
                document.getElementById("status").innerText = "🟡 Sin partidos en este momento";
            }

            document.getElementById("status").style.color = "#ffd166";

        } else {
            document.getElementById("status").innerText = `🟢 ${data.length} partidos activos`;
            document.getElementById("status").style.color = "#00ff88";
            const last = localStorage.getItem("last_update");
            if (last) {
                document.getElementById("status").innerText += ` • ${last}`;
            }

        }


        render(data);

    } catch (e) {
        console.log("⚠️ API caída, usando cache local");

        const cache = localStorage.getItem("partidos_cache");

        if (cache) {
            const data = JSON.parse(cache);

            // 🔴 estado offline
            const last = localStorage.getItem("last_update");

            if (last) {
                document.getElementById("status").innerText = `🔴 Offline • ${last}`;
            } else {
                document.getElementById("status").innerText = "🔴 Offline (sin historial)";
            }
            document.getElementById("status").style.color = "#ff4d4d";

            render(data);
        } else {
            container.innerHTML = "<div class='loader'>❌ Sin datos disponibles</div>";
        }
    }
}

function render(data) {
let html = "";

data.forEach(p => {
    html += `
    <div class="card">
        <div class="hora">
            🕒 ${p.hora}
            <span class="badge">LIVE</span>
        </div>

        <div class="partido">${p.partido}</div>

        <div class="canales">
            ${p.canales.map(c => `
                <a class="canal" href="${c.url}" target="_blank">
                    🔴 ${c.nombre}
                </a>
            `).join("")}
        </div>
    </div>
    `;
});

document.getElementById("app").innerHTML = html;
}
  
  // 🚀 cargar al inicio
load();
  
