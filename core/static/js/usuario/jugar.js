const _initGame = JSON.parse(document.getElementById('juego-data')?.textContent || '{}');
    const CSRF_TOKEN = (function() {
      const match = document.cookie.match(/csrftoken=([^;]+)/);
      if (match) return match[1];
      const input = document.querySelector('[name=csrfmiddlewaretoken]');
      return input ? input.value : '';
    })();
    const NIVEL_ID = _initGame.nivelId;
    const MUNDO_ISO = _initGame.mundoIso;
    const NUMERO_NIVEL = _initGame.numeroNivel;
    const FASES_DATA = _initGame.fasesData || [];

    let currentPhaseIdx = 0;
    let selectedCardIdx = null;
    let timeLeft = 45;
    let timerInterval = null;
    let isProcessing = false;

    function showToast(msg, duration = 3000) {
      const toast = document.getElementById('gameToast');
      const text = document.getElementById('toastMsg');
      if (toast && text) {
        text.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), duration);
      }
    }

    function renderCurrentPhase() {
      if (currentPhaseIdx >= FASES_DATA.length) {
        finalizarNivelConVictoria();
        return;
      }

      const fase = FASES_DATA[currentPhaseIdx];
      selectedCardIdx = null;
      isProcessing = false;

      // Header Plaque
      document.getElementById('casoHeaderTitle').textContent = `Caso #${fase.numero_fase}`;
      document.getElementById('casoHeaderSubtitle').textContent = `${MUNDO_ISO} — Nivel ${NUMERO_NIVEL} - Fase ${fase.numero_fase}`;

      // Scenario Box
      const contextText = fase.caso_contexto || fase.titulo_incidente || 'Analiza el caso y selecciona la carta adecuada.';
      document.getElementById('scenarioTextContent').textContent = contextText;

      // Cards Row
      const container = document.getElementById('cardsDeckContainer');
      let html = '';

      fase.cartas.forEach((c, idx) => {
        html += `
          <div class="iq-card-item" id="card-${idx}" onclick="seleccionarCarta(${idx});">
            <div class="iq-card-letter-diamond">
              <span>${c.letra}</span>
            </div>
            <div class="iq-card-art-box">
              <img src="${c.imagen_url}" alt="${c.nombre}" onerror="this.onerror=null; this.src='/static/img/cartas/carta_ciberseguridad.png';">
            </div>
            <div class="iq-card-title">${c.nombre}</div>
            <div class="iq-card-desc">${c.descripcion}</div>
          </div>
        `;
      });

      container.innerHTML = html;

      // Iniciar Temporizador de 45 segundos
      iniciarTemporizador(45);
    }

    function seleccionarCarta(idx) {
      if (isProcessing) return;

      selectedCardIdx = idx;
      const fase = FASES_DATA[currentPhaseIdx];

      fase.cartas.forEach((_, i) => {
        const el = document.getElementById(`card-${i}`);
        if (el) {
          if (i === idx) {
            el.classList.add('selected');
          } else {
            el.classList.remove('selected');
          }
        }
      });
    }

    function iniciarTemporizador(segundos) {
      clearInterval(timerInterval);
      timeLeft = segundos;
      actualizarDisplayReloj();

      timerInterval = setInterval(() => {
        timeLeft--;
        actualizarDisplayReloj();

        if (timeLeft <= 0) {
          clearInterval(timerInterval);
          tiempoAgotado();
        }
      }, 1000);
    }

    function actualizarDisplayReloj() {
      const display = document.getElementById('timerDisplay');
      if (!display) return;

      const mins = Math.floor(timeLeft / 60);
      const secs = timeLeft % 60;
      display.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

      if (timeLeft <= 10) {
        display.classList.add('urgent');
      } else {
        display.classList.remove('urgent');
      }
    }

    function tiempoAgotado() {
      if (isProcessing) return;
      isProcessing = true;

      // Registrar derrota por tiempo
      registrarDerrotaServer();

      document.getElementById('derrotaMsg').textContent = '¡Se ha agotado el tiempo de respuesta! La auditoría no toleró la demora.';
      const fase = FASES_DATA[currentPhaseIdx];
      const correcta = fase.cartas.find(c => c.es_correcta);
      if (correcta) {
        document.getElementById('derrotaSolucionNombre').textContent = `${correcta.nombre}: ${correcta.descripcion}`;
      }

      const modal = document.getElementById('modalDerrota');
      if (modal) modal.classList.add('show');
    }

    async function confirmarRespuesta() {
      if (isProcessing) return;

      if (selectedCardIdx === null) {
        showToast('⚠️ Por favor selecciona una de las cartas (A, B, C, D) para confirmar.');
        return;
      }

      isProcessing = true;
      clearInterval(timerInterval);

      const fase = FASES_DATA[currentPhaseIdx];
      const cartaElegida = fase.cartas[selectedCardIdx];
      const cardEl = document.getElementById(`card-${selectedCardIdx}`);

      if (cartaElegida.es_correcta) {
        // RESPUESTA CORRECTA
        if (cardEl) {
          cardEl.style.borderColor = '#10b981';
          cardEl.style.boxShadow = '0 0 35px #10b981, inset 0 0 20px #10b981';
        }

        if (currentPhaseIdx + 1 < FASES_DATA.length) {
          showToast('✓ ¡Control ISO correcto! Avanzando al siguiente caso...');
          setTimeout(() => {
            currentPhaseIdx++;
            renderCurrentPhase();
          }, 1200);
        } else {
          // Completó todas las fases del nivel con éxito
          showToast('✓ ¡Auditoría completada exitosamente!');
          setTimeout(() => {
            finalizarNivelConVictoria();
          }, 1000);
        }
      } else {
        // RESPUESTA INCORRECTA
        if (cardEl) {
          cardEl.style.borderColor = '#ef4444';
          cardEl.style.boxShadow = '0 0 35px #ef4444, inset 0 0 20px #ef4444';
        }

        registrarDerrotaServer();

        const correcta = fase.cartas.find(c => c.es_correcta);
        if (correcta) {
          document.getElementById('derrotaSolucionNombre').textContent = `${correcta.nombre}: ${correcta.descripcion}`;
        }
        document.getElementById('derrotaMsg').textContent = 'La carta seleccionada no mitiga esta vulnerabilidad adecuadamente.';

        setTimeout(() => {
          const modal = document.getElementById('modalDerrota');
          if (modal) modal.classList.add('show');
        }, 900);
      }
    }

    async function finalizarNivelConVictoria() {
      try {
        const response = await fetch(`/api/mapas/completar-nivel/${NIVEL_ID}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
          }
        });

        const data = await response.json();

        if (response.ok && data.success) {
          // Actualizar recompensas reales de la partida
          if (data.recompensas) {
            const expEl = document.getElementById('vicXpQty');
            if (expEl) expEl.textContent = `x${Number(data.recompensas.xp).toLocaleString()}`;
            const oroEl = document.getElementById('vicOroQty');
            if (oroEl) oroEl.textContent = `x${Number(data.recompensas.oro).toLocaleString()}`;
            const gemEl = document.getElementById('vicGemasQty');
            if (gemEl) gemEl.textContent = `x${Number(data.recompensas.gemas).toLocaleString()}`;
          }

          // Compatibilidad con IDs antiguos
          if (document.getElementById('vicXp')) document.getElementById('vicXp').textContent = `+${data.recompensas.xp} XP`;
          if (document.getElementById('vicOro')) document.getElementById('vicOro').textContent = `+${data.recompensas.oro} Oro`;
          if (document.getElementById('vicGemas')) document.getElementById('vicGemas').textContent = `+${data.recompensas.gemas} Gemas`;

          // Slot dinámico si subió de nivel
          if (data.progreso && data.progreso.subio_nivel) {
            const cardLvl = document.getElementById('vicCardLevelUp');
            const valLvl = document.getElementById('vicLevelUpVal');
            if (cardLvl && valLvl) {
              valLvl.textContent = `Nv. ${data.progreso.nivel}`;
              cardLvl.style.display = 'flex';
            }
          }

          // Subtítulo contextual
          const subTitle = document.getElementById('vicSubtitle');
          if (subTitle && data.nivel_superado) {
            subTitle.textContent = `Has completado todas las fases del Nivel ${data.nivel_superado.numero_nivel}: ${data.nivel_superado.titulo}`;
          }

          // Actualizar recursos de la topbar
          if (data.progreso) {
            document.getElementById('topbarOro').textContent = Number(data.progreso.oro).toLocaleString();
            document.getElementById('topbarGemas').textContent = Number(data.progreso.gemas).toLocaleString();
            document.getElementById('topbarXpFill').style.width = `${data.progreso.pct_xp}%`;
            document.getElementById('topbarXpText').textContent = `${Number(data.progreso.xp_en_nivel).toLocaleString()} / ${Number(data.progreso.xp_meta_nivel).toLocaleString()}`;
          }

          const worldNotice = document.getElementById('vicNewWorldBanner');
          if (data.nuevo_mundo_desbloqueado) {
            worldNotice.style.display = 'block';
            const worldNameEl = document.getElementById('vicNewWorldName');
            if (worldNameEl) worldNameEl.textContent = data.nuevo_mundo_desbloqueado;
          } else {
            worldNotice.style.display = 'none';
          }

          const modal = document.getElementById('modalVictoria');
          if (modal) modal.classList.add('show');
        } else {
          // Fallback en caso de error
          const modal = document.getElementById('modalVictoria');
          if (modal) modal.classList.add('show');
        }
      } catch (err) {
        const modal = document.getElementById('modalVictoria');
        if (modal) modal.classList.add('show');
      }
    }

    async function registrarDerrotaServer() {
      try {
        const response = await fetch(`/api/mapas/registrar-derrota/${NIVEL_ID}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
          }
        });
        const data = await response.json();
        if (data && data.recompensas) {
          const gemEl = document.getElementById('derrotaGemas');
          const oroEl = document.getElementById('derrotaOro');
          const xpEl = document.getElementById('derrotaXp');
          if (gemEl) gemEl.textContent = `+${data.recompensas.gemas || 0}`;
          if (oroEl) oroEl.textContent = `+${data.recompensas.oro || 0}`;
          if (xpEl) xpEl.textContent = `+${data.recompensas.xp || 0}`;
        }
      } catch (e) {
        console.error(e);
      }
    }

    function reiniciarPartidaActual() {
      document.getElementById('modalVictoria').classList.remove('show');
      document.getElementById('modalDerrota').classList.remove('show');
      currentPhaseIdx = 0;
      selectedCardIdx = null;
      renderCurrentPhase();
    }

    // Inicializar Gameplay al cargar la página
    document.addEventListener('DOMContentLoaded', () => {
      renderCurrentPhase();
    });
