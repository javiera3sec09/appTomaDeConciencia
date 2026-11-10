function filtrarTienda(cat, btn) {
      document.querySelectorAll('.iq-shop-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('#tiendaItemsGrid .iq-item-card').forEach(card => {
        if (cat === 'todos' || card.getAttribute('data-cat') === cat) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }
