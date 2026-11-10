const _initMapas = JSON.parse(document.getElementById('mapas-data')?.textContent || '{}');
    let mundosData = _initMapas.mundosData || [];
    let currentWorldIndex = 0;
    let currentActo = 1;
    let selectedNivelId = null;

    // Detectar índice inicial del mundo
    (function initActiveWorld() {
      const activeId = _initMapas.activeId;
      for (let i = 0; i < mundosData.length; i++) {
        if (mundosData[i].id === activeId) {
          currentWorldIndex = i;
          break;
        }
      }
    })();

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function showToast(msg, duration = 3000) {
      const toast = document.getElementById('gothicToast');
      const text = document.getElementById('toastMessage');
      if (toast && text) {
        text.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), duration);
      }
    }

    function openModal(id) {
      const m = document.getElementById(id);
      if (m) m.classList.add('show');
    }
    function closeModal(id) {
      const m = document.getElementById(id);
      if (m) m.classList.remove('show');
    }

    document.querySelectorAll('.iq-modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) overlay.classList.remove('show');
      });
    });

    // Renderizado reactivo de la línea SVG discontinua entre los 5 nodos
    function renderSvgDashedPath() {
      const svgGlow = document.getElementById('svgGlowPath');
      const svgDashed = document.getElementById('svgDashedPath');
      const currentWorld = mundosData[currentWorldIndex];

      if (!currentWorld || !currentWorld.niveles || currentWorld.niveles.length === 0 || !currentWorld.desbloqueado) {
        if (svgGlow) svgGlow.setAttribute('d', '');
        if (svgDashed) svgDashed.setAttribute('d', '');
        return;
      }

      // Filtrar niveles por acto actual (1 a 5, o 6 a 10)
      const visibleNiveles = currentWorld.niveles.filter(n => n.acto === currentActo || currentWorld.total_niveles <= 5);

      if (visibleNiveles.length < 2) {
        if (svgGlow) svgGlow.setAttribute('d', '');
        if (svgDashed) svgDashed.setAttribute('d', '');
        return;
      }

      // ViewBox 0 0 1000 1000
      const pts = visibleNiveles.map(n => ({
        x: (n.x / 100) * 1000,
        y: (n.y / 100) * 1000
      }));

      let d = `M ${pts[0].x} ${pts[0].y}`;
      for (let i = 1; i < pts.length; i++) {
        const p1 = pts[i - 1];
        const p2 = pts[i];
        const cx = (p1.x + p2.x) / 2;
        const cy = (p1.y + p2.y) / 2 - 8;
        d += ` Q ${cx} ${cy}, ${p2.x} ${p2.y}`;
      }

      if (svgGlow) svgGlow.setAttribute('d', d);
      if (svgDashed) svgDashed.setAttribute('d', d);
    }

    // Mini Castillo Gótico SVG para el Nodo Desbloqueado 1-1
    const MINI_CASTLE_SVG = `
      <svg class="iq-mini-castle-svg" viewBox="0 0 100 110" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Spire central -->
        <polygon points="50,4 42,28 58,28" fill="#d8b4fe" />
        <rect x="44" y="28" width="12" height="18" fill="#6b21a8" stroke="#c084fc" stroke-width="1.5" />
        <rect x="48" y="34" width="4" height="7" rx="2" fill="#fde047" />
        <!-- Spire izquierda -->
        <polygon points="26,16 20,34 32,34" fill="#a855f7" />
        <rect x="21" y="34" width="10" height="24" fill="#4c1d95" stroke="#a855f7" stroke-width="1.2" />
        <rect x="24" y="42" width="3.5" height="6" rx="1.5" fill="#fde047" />
        <!-- Spire derecha -->
        <polygon points="74,16 68,34 80,34" fill="#a855f7" />
        <rect x="69" y="34" width="10" height="24" fill="#4c1d95" stroke="#a855f7" stroke-width="1.2" />
        <rect x="72" y="42" width="3.5" height="6" rx="1.5" fill="#fde047" />
        <!-- Muralla almenada central -->
        <path d="M 28 50 L 32 50 L 32 46 L 38 46 L 38 50 L 44 50 L 44 46 L 56 46 L 56 50 L 62 50 L 62 46 L 68 46 L 68 50 L 72 50 L 72 78 L 28 78 Z" fill="#3b0764" stroke="#c084fc" stroke-width="1.5" />
        <!-- Ventanas arcanas -->
        <rect x="36" y="56" width="6" height="10" rx="3" fill="#e879f9" />
        <rect x="58" y="56" width="6" height="10" rx="3" fill="#e879f9" />
        <!-- Portal de entrada con arco gótico -->
        <path d="M 44 78 L 44 65 Q 50 60 56 65 L 56 78 Z" fill="#140628" stroke="#d8b4fe" stroke-width="1.5" />
        <path d="M 46 78 L 46 67 Q 50 63 54 67 L 54 78 Z" fill="#a855f7" opacity="0.8" />
        <!-- Almenas inferiores y contrafuertes -->
        <rect x="18" y="56" width="12" height="24" fill="#2e1065" stroke="#a855f7" stroke-width="1" />
        <rect x="70" y="56" width="12" height="24" fill="#2e1065" stroke="#a855f7" stroke-width="1" />
      </svg>
    `;

    // Renderizar los Nodos del Mundo Actual
    function renderWorldNodes() {
      const currentWorld = mundosData[currentWorldIndex];
      const container = document.getElementById('nodesContainer');
      const bannerOrden = document.getElementById('worldBannerOrden');
      const bannerName = document.getElementById('worldBannerName');
      const bannerDesc = document.getElementById('worldBannerDesc');
      const btnPrev = document.getElementById('btnPrevWorld');
      const btnNext = document.getElementById('btnNextWorld');
      const actTabsBar = document.getElementById('actTabsBar');

      if (!currentWorld || !container) return;

      if (btnPrev) btnPrev.disabled = (currentWorldIndex === 0);
      if (btnNext) btnNext.disabled = (currentWorldIndex === mundosData.length - 1);

      if (bannerOrden) bannerOrden.textContent = `Mundo ${currentWorld.orden}`;
      if (bannerName) {
        let lockIcon = !currentWorld.desbloqueado ? ' <i class="bi bi-lock-fill" style="color: #f87171; font-size: 16px;" title="Mundo Bloqueado"></i>' : '';
        bannerName.innerHTML = `${currentWorld.nombre_fantasia}${lockIcon}`;
      }
      if (bannerDesc) bannerDesc.textContent = currentWorld.descripcion_narrativa;

      // Mostrar selector de actos si el mundo tiene más de 5 niveles (ej: 10 niveles)
      if (actTabsBar) {
        if (currentWorld.total_niveles > 5 && currentWorld.desbloqueado) {
          actTabsBar.style.display = 'flex';
        } else {
          actTabsBar.style.display = 'none';
        }
      }

      if (!currentWorld.desbloqueado) {
        container.innerHTML = `
          <div style="position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%); text-align: center; background: rgba(15, 10, 36, 0.94); border: 2px solid #ef4444; border-radius: 20px; padding: 28px 36px; box-shadow: 0 0 40px rgba(239, 68, 68, 0.5); backdrop-filter: blur(10px); z-index: 35;">
            <i class="bi bi-lock-fill" style="font-size: 44px; color: #f87171; filter: drop-shadow(0 0 10px #ef4444); display: block; margin-bottom: 12px;"></i>
            <h3 style="font-family: 'Cinzel', serif; font-size: 20px; color: #fff; margin-bottom: 8px;">MUNDO BLOQUEADO</h3>
            <p style="color: #cbd5e1; font-size: 13.5px; max-width: 320px; line-height: 1.4;">Para desbloquear este mapa debes superar primero todos los niveles del Mundo ${currentWorld.orden - 1}.</p>
          </div>
        `;
        renderSvgDashedPath();
        return;
      }

      // Filtrar niveles del acto seleccionado (1..5 o 6..10)
      const nivelesVisibles = currentWorld.niveles.filter(n => n.acto === currentActo || currentWorld.total_niveles <= 5);

      let html = '';
      nivelesVisibles.forEach((n, idx) => {
        let isFirstOrActual = (n.estado_progreso === 'actual' || (n.numero_nivel === 1 && !n.ha_ganado));
        let nodeBody = '';

        if (isFirstOrActual || n.estado_progreso === 'completado') {
          // NODO DESBLOQUEADO O COMPLETADO (Mini Castillo + Altar + Placa + 3 Estrellas)
          nodeBody = `
            <div class="iq-node-1-1-wrap">
              ${MINI_CASTLE_SVG}
              <div class="iq-altar-pedestal">
                <div class="iq-node-plaque">${n.codigo_nivel}</div>
                <div class="iq-altar-stars-row">
                  <i class="bi bi-star-fill iq-altar-star"></i>
                  <i class="bi bi-star-fill iq-altar-star"></i>
                  <i class="bi bi-star-fill iq-altar-star"></i>
                </div>
              </div>
            </div>
          `;
        } else {
          // NODOS BLOQUEADOS (Pedestal con Cúpula + Candado + Placa de código)
          nodeBody = `
            <div class="iq-locked-pedestal-wrap">
              <div class="iq-locked-dome">
                <i class="bi bi-lock-fill"></i>
              </div>
              <div class="iq-locked-stone-base">
                <div class="iq-locked-plaque">${n.codigo_nivel}</div>
              </div>
            </div>
          `;
        }

        let statusText = isFirstOrActual ? 'Desbloqueado' : (n.estado_progreso === 'completado' ? 'Superado ★★★' : '🔒 Bloqueado');

        html += `
          <div class="iq-bridge-node"
               style="left: ${n.x}%; top: ${n.y}%;"
               onclick="clickNodoNivel(${n.id});"
               data-nivel-id="${n.id}">
            ${nodeBody}
            <!-- Tarjeta HUD al pasar el cursor con los datos reales de la BD -->
            <div class="iq-node-hud-card">
              <div class="iq-hud-title">Nivel ${n.codigo_nivel}: ${n.titulo}</div>
              <div class="iq-hud-meta-row">
                <span class="iq-hud-status-badge ${n.estado_progreso}">${statusText}</span>
                <span style="color: #c084fc; font-size: 11px;">${n.dificultad_display || n.dificultad}</span>
                ${n.tipo === 'jefe' ? '<span style="color: #f87171; font-size: 10px; font-weight: 800;">[JEFE]</span>' : ''}
              </div>
              <div class="iq-hud-rewards">
                <span><i class="bi bi-coin" style="color: #fbbf24;"></i> +${n.recompensa_oro}</span>
                <span><i class="bi bi-gem" style="color: #ec4899;"></i> +${n.recompensa_gemas}</span>
                <span><i class="bi bi-stars" style="color: #c084fc;"></i> +${n.recompensa_xp} XP</span>
              </div>
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
      renderSvgDashedPath();
    }

    function cambiarActo(actoNum) {
      currentActo = actoNum;
      document.getElementById('tabActo1').className = `iq-act-tab-btn ${actoNum === 1 ? 'active' : ''}`;
      document.getElementById('tabActo2').className = `iq-act-tab-btn ${actoNum === 2 ? 'active' : ''}`;
      renderWorldNodes();
    }

    function cambiarMundoPrev() {
      if (currentWorldIndex > 0) {
        currentWorldIndex--;
        currentActo = 1;
        renderWorldNodes();
      }
    }

    function cambiarMundoNext() {
      if (currentWorldIndex < mundosData.length - 1) {
        const nextWorld = mundosData[currentWorldIndex + 1];
        if (!nextWorld.desbloqueado) {
          showToast(`🔒 El Mundo ${nextWorld.orden} (${nextWorld.codigo_iso}) está bloqueado. Completa todos los niveles del Mundo actual para desbloquearlo.`);
        }
        currentWorldIndex++;
        currentActo = 1;
        renderWorldNodes();
      }
    }

    function clickNodoNivel(nivelId) {
      const currentWorld = mundosData[currentWorldIndex];
      if (!currentWorld) return;

      const nivel = currentWorld.niveles.find(n => n.id === nivelId);
      if (!nivel) return;

      if (nivel.estado_progreso === 'bloqueado') {
        showToast(`🔒 Nivel ${nivel.codigo_nivel} Bloqueado. Debes superar el nivel anterior para desbloquearlo.`);
        return;
      }

      // Redirigir directamente al gameplay del nivel seleccionado
      window.location.href = `/jugar/${nivel.id}/`;
    }

    // Jugar el nivel activo actual al pulsar el botón [⚔️ Jugar]
    function jugarNivelActual() {
      const currentWorld = mundosData[currentWorldIndex];
      if (!currentWorld || !currentWorld.desbloqueado) {
        showToast('🔒 Este mundo se encuentra bloqueado actualmente.');
        return;
      }

      // Buscar el primer nivel en estado 'actual' listo para jugar
      const nivelActual = currentWorld.niveles.find(n => n.estado_progreso === 'actual') || currentWorld.niveles[0];
      if (nivelActual) {
        window.location.href = `/jugar/${nivelActual.id}/`;
      }
    }

    // Completar el nivel con éxito
    async function completarNivelVictoria() {
      if (!selectedNivelId) return;

      const btn = document.getElementById('btnEjecutarVictoria');
      btn.disabled = true;
      btn.innerHTML = '<i class="bi bi-hourglass-split"></i> <span>Verificando Controles ISO...</span>';

      try {
        const response = await fetch(`/api/mapas/completar-nivel/${selectedNivelId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          }
        });

        const data = await response.json();

        if (response.ok && data.success) {
          closeModal('modalNivelInfo');

          mundosData = data.mundos_data;

          document.getElementById('topbarOro').textContent = Number(data.progreso.oro).toLocaleString();
          document.getElementById('topbarGemas').textContent = Number(data.progreso.gemas).toLocaleString();
          document.getElementById('topbarXpFill').style.width = `${data.progreso.pct_xp}%`;
          document.getElementById('topbarXpText').textContent = `${Number(data.progreso.xp_en_nivel).toLocaleString()} / ${Number(data.progreso.xp_meta_nivel).toLocaleString()}`;

          // Actualizar recompensas reales de la partida
          if (data.recompensas) {
            const expEl = document.getElementById('vicXpQty');
            if (expEl) expEl.textContent = `x${Number(data.recompensas.xp).toLocaleString()}`;
            const oroEl = document.getElementById('vicOroQty');
            if (oroEl) oroEl.textContent = `x${Number(data.recompensas.oro).toLocaleString()}`;
            const gemEl = document.getElementById('vicGemasQty');
            if (gemEl) gemEl.textContent = `x${Number(data.recompensas.gemas).toLocaleString()}`;
          }

          if (document.getElementById('vicXp')) document.getElementById('vicXp').textContent = `+${data.recompensas.xp}`;
          if (document.getElementById('vicOro')) document.getElementById('vicOro').textContent = `+${data.recompensas.oro}`;
          if (document.getElementById('vicGemas')) document.getElementById('vicGemas').textContent = `+${data.recompensas.gemas}`;

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
          const subTitle = document.getElementById('victorySubtitle');
          if (subTitle && data.nivel_superado) {
            subTitle.textContent = `Has completado todas las fases del Nivel ${data.nivel_superado.numero_nivel}: ${data.nivel_superado.titulo}`;
          }

          const worldNotice = document.getElementById('victoryWorldUnlockedNotice');
          if (data.nuevo_mundo_desbloqueado) {
            worldNotice.style.display = 'block';
            const worldNameEl = document.getElementById('vicMapNewWorldName');
            if (worldNameEl) worldNameEl.textContent = data.nuevo_mundo_desbloqueado;
            else worldNotice.innerHTML = `🌟 ¡HAS DESBLOQUEADO EL SIGUIENTE MUNDO: <strong>${data.nuevo_mundo_desbloqueado}</strong>! 🌟`;
          } else {
            worldNotice.style.display = 'none';
          }

          openModal('modalVictoria');
          renderWorldNodes();
          showToast(`✓ ¡Nivel superado con éxito! Siguiente nivel desbloqueado.`);
        } else {
          showToast(`Error: ${data.error || 'No se pudo completar el nivel.'}`);
        }
      } catch (err) {
        showToast('Error de conexión con el servidor.');
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-swords"></i> <span>COMENZAR AUDITORÍA</span>';
      }
    }

    async function reiniciarProgresoPartidasPrueba() {
      if (!confirm('¿Deseas reiniciar tus partidas ganadas para probar el desbloqueo de Nivel 1 en adelante?')) return;

      try {
        const response = await fetch('/api/mapas/reiniciar-partidas/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          }
        });
        const data = await response.json();
        if (data.success) {
          mundosData = data.mundos_data;
          currentWorldIndex = 0;
          currentActo = 1;
          renderWorldNodes();
          showToast('✓ Progreso reiniciado: Solo el Nivel 1-1 está disponible ahora.');
        }
      } catch (err) {
        showToast('Error al reiniciar progreso.');
      }
    }

    async function guardarPerfilJugador() {
      const input = document.getElementById('inputModalAlias');
      const statusMsg = document.getElementById('profileStatusMsg');
      const nuevoAlias = input.value.trim();
      if (!nuevoAlias) return;

      try {
        const resp = await fetch('/api/player/update-profile/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: JSON.stringify({ alias: nuevoAlias })
        });
        const res = await resp.json();
        if (res.success) {
          statusMsg.style.color = '#34d399';
          statusMsg.textContent = '✓ Perfil actualizado';
          document.getElementById('topbarAlias').textContent = res.alias;
          setTimeout(() => closeModal('modalPerfil'), 900);
        } else {
          statusMsg.style.color = '#f87171';
          statusMsg.textContent = res.error || 'Error';
        }
      } catch (e) {
        statusMsg.style.color = '#f87171';
        statusMsg.textContent = 'Error de conexión';
      }
    }

    function seleccionarAvatarRapido(url) {
      const img = document.getElementById('profileModalAvatarImg');
      if (img) img.src = url;
      closeModal('modalColeccion');
      openModal('modalPerfil');
    }

    window.addEventListener('load', () => {
      renderWorldNodes();
    });

    window.addEventListener('resize', () => {
      renderSvgDashedPath();
    });
