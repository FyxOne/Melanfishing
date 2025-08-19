// Melanfishing — HTML5 Canvas порт
// Поведение и тайминги перенесены из оригинальных pygame-скриптов.
// Файлы ресурсов ожидаются в папке ./resources

(() => {
  const W = 1280, H = 720;
  const DarkPurple = "#0f0032";
  const LightYellow = "rgb(255,255,100)";
  /** @type {HTMLCanvasElement} */
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');
  // Отключаем жесты браузера (скролл/зуум) для стабильных touch-событий
  canvas.style.touchAction = 'none';

  // --- Utils ---------------------------------------------------------------
  function resourcePath(p) { return p; } // в браузере — относительный путь без преобразований
  function nowMs() { return performance.now(); }

  // --- Audio subsystem (каналы) -------------------------------------------
  const CHANNELS = { MUSIC:0, AMBIENT:1, ENGINE:2, COOKING:3, FX:4 };
  class Channel {
    constructor() { this.node = new Audio(); this.node.loop = false; this.busy = false; }
    play(src, {loop=false, volume=1.0}={}) {
      if (!src) return;
      this.node.src = src;
      this.node.loop = loop;
      this.node.volume = volume;
      this.node.currentTime = 0;
      this.node.play().catch(()=>{});
      this.busy = true;
    }
    stop() { try { this.node.pause(); } catch{} this.busy=false; }
    setVolume(v) { this.node.volume = Math.max(0, Math.min(1, v)); }
    get_busy(){ return !this.node.paused; }
  }
  const audio = {
    ch: [new Channel(), new Channel(), new Channel(), new Channel(), new Channel()],
    channel(i){ return this.ch[i]; },
    stop_all(){ this.ch.forEach(c=>c.stop()); },
    play_music(volume=0.15){
      // resources/under_rian.ogg
      this.channel(CHANNELS.MUSIC).play(resourcePath('resources/under_rian.ogg'), {loop:true, volume});
    },
  };

  // --- Sprites/Images ------------------------------------------------------
  function loadImage(src) {
    return new Promise(res=>{
      const img = new Image();
      img.onload = ()=>res(img);
      img.onerror = ()=>res(null);
      img.src = src;
    });
  }

  // Preload frequently used textures
  const IMAGES = {};
  const toLoad = [
    ['logo', 'resources/logo.png'],
    ['car', 'resources/car.png'],
    ['f1', 'resources/fishing1.png'],
    ['f2', 'resources/fishing2.png'],
    ['f3', 'resources/fishing3.png'],
    ['pan1', 'resources/pan1.png'],
    ['pan2', 'resources/pan2.png'],
    ['add_fire', 'resources/add_fire.png'],
    ['arrow_btn', 'resources/arrow_btn.png'],
    ['a_btn', 'resources/a_btn.png'],
    ['b_btn', 'resources/b_btn.png'],
  ];

  // Sounds
  const SOUNDS = {
    klujet: 'resources/klujet.mp3',
    katushka: 'resources/katushka.mp3',
    rain: 'resources/rain.mp3',
    car_sound: 'resources/car_sound.mp3',
    frying: 'resources/frying.mp3',
    stir: 'resources/stir.mp3',
  };

  // --- Touch controls ------------------------------------------------------
  class TouchControls {
    constructor(sw=W, sh=H) {
      this.sw = sw; this.sh = sh;
      const size = 80, margin = 20;
      this.btn_left = {x: margin, y: sh - margin - size*2, w: size, h: size};
      this.btn_right= {x: margin + size*2, y: sh - margin - size*2, w:size,h:size};
      this.btn_up   = {x: margin + size, y: sh - margin - size*3, w:size,h:size};
      this.btn_down = {x: margin + size, y: sh - margin - size,   w:size,h:size};
      const ab_y = sh - margin - size*2;
      this.btn_a    = {x: sw - margin - size, y: ab_y, w:size,h:size};
      this.btn_b    = {x: sw - margin - size*2 - margin, y: ab_y, w:size,h:size};
      this.key_w=false; this.key_a=false; this.key_s=false; this.key_d=false;
      this.mouse_left=false; this.mouse_right=false;
      this.activeTouches = new Map();
    }
    rectContains(r, px, py){ return px>=r.x && py>=r.y && px<=r.x+r.w && py<=r.y+r.h; }
    _recompute(){
      this.key_w=this.key_a=this.key_s=this.key_d=false;
      this.mouse_left=false; this.mouse_right=false;
      let anyFreeTouch = false;
      for (const {x,y} of this.activeTouches.values()){
        let onBtn=false;
        if (this.rectContains(this.btn_up,x,y)){ this.key_w = true; onBtn=true; }
        if (this.rectContains(this.btn_down,x,y)){ this.key_s = true; onBtn=true; }
        if (this.rectContains(this.btn_left,x,y)){ this.key_a = true; onBtn=true; }
        if (this.rectContains(this.btn_right,x,y)){ this.key_d = true; onBtn=true; }
        if (this.rectContains(this.btn_a,x,y)){ this.mouse_left = true; onBtn=true; }
        if (this.rectContains(this.btn_b,x,y)){ this.mouse_right = true; onBtn=true; }
        if (!onBtn) anyFreeTouch = true;
      }
      // Любой палец вне виртуальных кнопок = ЛКМ по экрану
      if (anyFreeTouch) this.mouse_left = true;
    }
    handleTouchStart(id,x,y){ this.activeTouches.set(id,{x,y}); this._recompute(); }
    handleTouchMove(id,x,y){ if (this.activeTouches.has(id)){ this.activeTouches.set(id,{x,y}); this._recompute(); } }
    handleTouchEnd(id){ this.activeTouches.delete(id); this._recompute(); }
    draw(g){
      g.save();
      const arrow = IMAGES.arrow_btn;
      if (arrow) {
        const render = (r, rot=0)=>{
          g.save();
          g.translate(r.x + r.w/2, r.y + r.h/2);
          g.rotate(rot*Math.PI/180);
          g.drawImage(arrow, -r.w/2, -r.h/2, r.w, r.h);
          g.restore();
        };
        render(this.btn_up, 0);
        render(this.btn_down, 180);
        render(this.btn_left, -90);
        render(this.btn_right, 90);
      } else {
        g.fillStyle = "rgba(255,255,255,.3)";
        [this.btn_up,this.btn_down,this.btn_left,this.btn_right].forEach(r=>g.fillRect(r.x,r.y,r.w,r.h));
      }
      if (IMAGES.a_btn) g.drawImage(IMAGES.a_btn, this.btn_a.x, this.btn_a.y, this.btn_a.w, this.btn_a.h);
      else { g.fillStyle="rgba(255,255,255,.3)"; g.fillRect(this.btn_a.x,this.btn_a.y,this.btn_a.w,this.btn_a.h); }
      if (IMAGES.b_btn) g.drawImage(IMAGES.b_btn, this.btn_b.x, this.btn_b.y, this.btn_b.w, this.btn_b.h);
      else { g.fillStyle="rgba(255,255,255,.3)"; g.fillRect(this.btn_b.x,this.btn_b.y,this.btn_b.w,this.btn_b.h); }
      g.restore();
    }
  }

  // --- Input (клавиатура/мышь/тач) ---------------------------------------
  const keys = { w:false, a:false, s:false, d:false, alt:false };
  const mouseButtons = { left:false, right:false };
  let mousePos = { x:0, y:0 };
  const controls = new TouchControls(W,H);

  window.addEventListener('keydown', (e)=>{
    if (e.code==='KeyW') keys.w=true;
    if (e.code==='KeyA') keys.a=true;
    if (e.code==='KeyS') keys.s=true;
    if (e.code==='KeyD') keys.d=true;
    if (e.code==='AltLeft') keys.alt=true;
  });
  window.addEventListener('keyup', (e)=>{
    if (e.code==='KeyW') keys.w=false;
    if (e.code==='KeyA') keys.a=false;
    if (e.code==='KeyS') keys.s=false;
    if (e.code==='KeyD') keys.d=false;
    if (e.code==='AltLeft') keys.alt=false;
  });
  canvas.addEventListener('mousemove', (e)=>{
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    mousePos.x = (e.clientX - rect.left) * scaleX;
    mousePos.y = (e.clientY - rect.top) * scaleY;
  });
  canvas.addEventListener('mousedown', (e)=>{
    if (e.button===0) mouseButtons.left=true;
    if (e.button===2) mouseButtons.right=true;
  });
  canvas.addEventListener('mouseup', (e)=>{
    if (e.button===0) mouseButtons.left=false;
    if (e.button===2) mouseButtons.right=false;
  });
  canvas.addEventListener('contextmenu', (e)=>e.preventDefault());

  // Touch -> виртуальные кнопки + симуляция ЛКМ/ПКМ
  const touchHandler = (e) => {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    // собираем координаты и обновляем контролы
    for (const t of e.changedTouches){
      const x = (t.clientX - rect.left)*scaleX;
      const y = (t.clientY - rect.top)*scaleY;
      mousePos.x = x;
      mousePos.y = y;

      if (e.type==='touchstart') controls.handleTouchStart(t.identifier,x,y);
      if (e.type==='touchmove') controls.handleTouchMove(t.identifier,x,y);
      if (e.type==='touchend' || e.type==='touchcancel') controls.handleTouchEnd(t.identifier);
    }

    // синхронизируем кнопки мыши по результату hit-тестов
    mouseButtons.left  = controls.mouse_left;
    mouseButtons.right = controls.mouse_right;

    e.preventDefault();
  };
  canvas.addEventListener('touchstart', touchHandler, {passive:false});
  canvas.addEventListener('touchmove', touchHandler, {passive:false});
  canvas.addEventListener('touchend', touchHandler, {passive:false});
  canvas.addEventListener('touchcancel', touchHandler, {passive:false});

  // --- Menu buttons -------------------------------------------------------
  class Button {
    constructor(x=0,y=0,w=250,h=50,text="New button") {
      this.x=x; this.y=y; this.w=w; this.h=h; this.text=text;
      this.rect = {x,y,w,h};
    }
    setPosition(x,y){ this.x=x; this.y=y; this.rect.x=x; this.rect.y=y; }
    draw(g, color){
      g.fillStyle = color; g.fillRect(this.x,this.y,this.w,this.h);
      g.fillStyle = DarkPurple; g.font = "30px EpilepsySans";
      g.textAlign="center"; g.textBaseline="middle";
      g.fillText(this.text, this.x+this.w/2, this.y+this.h/2);
    }
    contains(px,py){ return px>=this.x && py>=this.y && px<=this.x+this.w && py<=this.y+this.h; }
  }
  const play_button = new Button(W/2 - 250/2, 300, 250, 50, "Play");
  const quit_button = new Button(W/2 - 250/2, 370, 250, 50, "Quit");

  // --- Splashes -----------------------------------------------------------
  const splashes = [
    "Здоровенный язь","Ебать ты окунь","Придумайте сплешей","Точно расслабляющая игра?","Разраб дебил",
    "Also try Quadix3D","Python is trash","Рыба нахуй!","Батон ис воркинг","ИИ придумал этот сплеш",
    "Сделано на коленке","404 Рыба не найдена","Alt+F4 = золотая рыбка","Powered by костыли",
    "Продам гараж","Поставь чайник, заебал","Бесплатно, потому что никому не надо",
    "Кстати, в main.py кейлоггер зашит","Выпрями спину","Тут могла быть ваша реклама",
    "Ты чё, опять тут?","Сохранение не предусмотрено"
  ];
  function randomSplash(){ return splashes[Math.floor(Math.random()*splashes.length)]; }
  let splash = randomSplash();
  document.title = `Melanfishing | ${splash}`;

  // --- Fishing state ------------------------------------------------------
  class Fishing {
    constructor(){
      this.isFishing=false;
      this.isKeyPressed=false;
      this.posx=55;
      this.direction=0;
      this.arrow_x=140;
      this.zone = {x:this.posx, y:55, w:30, h:40};
      this.arrow= {x:this.arrow_x, y:50, w:5, h:50};
      this.points=0; this.fish=0;
      this.start_time = nowMs();
      this.startstart_time = nowMs();
      this.dt=0; this.wait_time=5;
      this.pizda=0; this.lock=0; this.start=0; this.reaction=0; this.fuck_u=0; this.meow=0;
      this.text_cache = `My fishies: ${this.fish}`;
      this.arrow_speed=0.1;
      this.zone_speed=0.05;
      this.player_texture = IMAGES.f1;
      this.katushkaLoop = new Channel();
    }
    getFishes(){ return this.fish; }
    keybinds(mouse){
      const pipipi = this.wait_time - Math.floor((nowMs() - this.startstart_time)/1000);
      if (pipipi <= 0){
        if (this.pizda === 0){
          this.start = performance.now()/1000;
          this.pizda = 1;
          audio.channel(CHANNELS.FX).play(SOUNDS.klujet);
        }
        if (this.lock !== 1){
          this.fuck_u = performance.now()/1000 - this.start;
          if (mouse.right){
            this.reaction = performance.now()/1000 - this.start;
            this.arrow_x = 140; this.posx = 55;
            this.zone.x=this.posx; this.zone.y=55;
            this.arrow.x=this.arrow_x; this.arrow.y=50;
            if (this.reaction < 1){
              // крутится катушка
              this.katushkaLoop.play(SOUNDS.katushka, {loop:true, volume:0.1});
              this.player_texture = IMAGES.f2;
              if (!this.isKeyPressed){ this.isKeyPressed = true; this.lock=1; if (!this.isFishing) this.isFishing = true; }
            } else {
              this.pizda = 0;
              audio.channel(CHANNELS.FX).stop();
              this.startstart_time = nowMs();
            }
          } else {
            this.isKeyPressed = false;
          }
        }
      }
    }
    rectsIntersect(a,b){ return a.x<b.x+b.w && a.x+a.w>b.x && a.y<b.y+b.h && a.y+a.h>b.y; }
    random(){
      const pi_pi = 1 - Math.floor((nowMs() - this.start_time)/1000);
      if (pi_pi <= 0){ this.start_time = nowMs(); this.direction = Math.random()<0.5?1:2; }
      if (this.direction === 1){
        this.posx += this.zone_speed * this.dt;
        if (this.posx > 220) this.direction = 2;
      }
      if (this.direction === 2){
        this.posx -= this.zone_speed * this.dt;
        if (this.posx < 60) this.direction = 1;
      }
    }
    update(keys, mouse, dt){
      this.dt = dt;
      if (this.arrow_x > 300 || this.arrow_x < 40) this.arrow_x = 140;
      (this.rectsIntersect(this.zone,this.arrow)) ? (this.points = Math.min(240, this.points+1)) : (this.points = Math.max(-0.1, this.points-1));
      if (this.points > 239){
        this.points = 0; this.fish += 1; this.isFishing = false; this.player_texture = IMAGES.f1; this.startstart_time = nowMs();
        this.katushkaLoop.stop();
        audio.channel(CHANNELS.FX).play(SOUNDS.klujet);
        this.wait_time = Math.floor(3 + Math.random()*8);
        this.arrow_x = 140; this.posx = 55;
        this.zone.x=this.posx; this.zone.y=55;
        this.arrow.x=this.arrow_x; this.arrow.y=50;
        this.pizda=0; this.lock=0;
        this.text_cache = `My fishies: ${this.fish}`;
      }
      if (this.points === 227) this.player_texture = IMAGES.f3;

      if (this.isFishing){
        if (mouse.left){ if (this.arrow_x <= 290) this.arrow_x += this.arrow_speed * this.dt; }
        else { if (this.arrow_x >= 55) this.arrow_x -= this.arrow_speed * this.dt; if (this.arrow.x < 40) this.arrow_x = 150; }
      }
      this.zone.x=this.posx; this.zone.y=55;
      this.arrow.x=this.arrow_x; this.arrow.y=50;
    }
    draw(g){
      // рамки
      g.strokeStyle = LightYellow; g.lineWidth = 2;
      // верхняя рамка
      g.beginPath(); g.moveTo(50,50); g.lineTo(300,50); g.moveTo(50,100); g.lineTo(300,100); g.moveTo(50,50); g.lineTo(50,100); g.moveTo(300,50); g.lineTo(300,100); g.stroke();
      // нижняя рамка
      g.beginPath(); g.moveTo(50,150); g.lineTo(300,150); g.moveTo(50,200); g.lineTo(300,200); g.moveTo(50,150); g.lineTo(50,200); g.moveTo(300,150); g.lineTo(300,200); g.stroke();
      // прогресс
      g.fillStyle = LightYellow; g.fillRect(55,155, this.points, 40);
      // зона и стрелка
      g.fillStyle = LightYellow; g.fillRect(this.zone.x, this.zone.y, this.zone.w, this.zone.h);
      g.fillStyle = "red"; g.fillRect(this.arrow.x, this.arrow.y, this.arrow.w, this.arrow.h);
    }
    force_draw(g){
      // фон/персонаж
      if (this.player_texture) g.drawImage(this.player_texture, 0,0, W,H);
      // текст
      g.fillStyle = "rgb(255,255,100)"; g.font = "30px EpilepsySans"; g.fillText(this.text_cache, W-200, 50);
      if (this.lock===0 && this.pizda===1 && this.fuck_u <= 1){
        g.fillStyle = "rgb(255,255,100)"; g.fillText(this.fuck_u.toFixed(2), 500, 100);
      }
      if (this.lock===0 && this.pizda===1 && this.fuck_u > 1){
        g.fillStyle = "rgb(255,0,0)"; g.fillText(this.fuck_u.toFixed(2), 500, 100);
      }
    }
  }

  // --- Driving state ------------------------------------------------------
  class Driving {
    constructor(){
      this.direction=0; this.posx=365;
      this.start_time = nowMs();
      this.car_speed = 0; this.direction_speed = this.car_speed*0.3;
      this.arrow_x = 985;
      this.car_model = {x:this.posx, y:365, w:500, h:250};
      this.car_texture = IMAGES.car;
      this.arrow = {x:this.arrow_x, y:50, w:5, h:50};
      this.dt=0; this.points=0;
      this.engine_playing=false;
      this.engine = new Channel();
    }
    getPoints(){ return this.points; }
    _ensure_engine(){
      if (!this.engine_playing){
        this.engine.play(SOUNDS.car_sound, {loop:true, volume:0.0});
        this.engine_playing=true;
      }
    }
    _update_engine_volume(){
      if (!this.engine_playing) return;
      this.engine.setVolume(Math.max(0, Math.min(1, this.car_speed * 0.5)));
    }
    random(){
      const pi_pi = 1 - Math.floor((nowMs() - this.start_time)/1000);
      if (pi_pi <= 0){ this.start_time = nowMs(); this.direction = Math.random()<0.5?1:2; }
      if (this.direction===1){
        if (this.posx <= 780 && this.direction_speed>0){ this.posx += this.direction_speed * this.dt; }
      } else if (this.direction===2){
        if (this.posx >= 0 && this.direction_speed>0){ this.posx -= this.direction_speed * this.dt; }
      }
    }
    update(keys, mouse, dt){
      this.dt = dt;
      this._ensure_engine();
      if (keys.d){ if (this.posx<=780 && this.car_speed>=0) this.posx += this.car_speed * this.dt; }
      if (keys.a){ if (this.posx>=0 && this.car_speed>=0) this.posx -= this.car_speed * this.dt; }
      if (keys.w){
        if (this.car_speed <= 1) { this.car_speed += 0.01; this.direction_speed = this.car_speed*0.3; }
        if (this.car_speed > 1) this.car_speed = 1;
        if (this.arrow_x >= 985 && this.arrow_x <= 1220) this.arrow_x = this.car_speed * 235 + 985;
      }
      if (keys.s){
        if (this.car_speed >= 0){ this.car_speed -= 0.01; this.direction_speed = this.car_speed*0.3; }
        if (this.car_speed < 0) this.car_speed = 0;
        if (this.direction_speed < 0) this.direction_speed = 0;
        if (this.arrow_x >= 985 && this.arrow_x <= 1220) this.arrow_x = this.car_speed * 235 + 985;
      }
      this.car_model.x = this.posx; this.car_model.y = 365;
      this.arrow.x = this.arrow_x; this.arrow.y = 50;

      if (this.points <= 241){
        if (this.posx >= 280 && this.posx <= 500) this.points += this.car_speed * 0.5;
        else { if (this.points >= 0) this.points -= 5; }
      }
      this._update_engine_volume();
    }
    draw(g){
      g.strokeStyle = LightYellow; g.lineWidth = 2;
      // линии дороги
      g.beginPath();
      g.moveTo(480,0); g.lineTo(320,720);
      g.moveTo(800,0); g.lineTo(960,720);
      g.lineWidth = 10; g.moveTo(160,0); g.lineTo(0,180);
      g.stroke();
      // спидометр
      g.lineWidth = 1.5;
      g.beginPath();
      g.moveTo(980,50); g.lineTo(1230,50);
      g.moveTo(980,100); g.lineTo(1230,100);
      g.moveTo(980,50); g.lineTo(980,100);
      g.moveTo(1230,50); g.lineTo(1230,100);
      g.stroke();
      g.fillStyle = LightYellow; g.fillRect(985,55, this.points, 40);
      g.fillStyle = "red"; g.fillRect(this.arrow.x, this.arrow.y, this.arrow.w, this.arrow.h);
      if (this.car_texture)
        g.drawImage(this.car_texture, this.car_model.x, this.car_model.y, this.car_model.w, this.car_model.h);
    }
    stop_audio(){ this.engine.stop(); }
  }

  // --- Cooking state ------------------------------------------------------
  class Cooking {
    constructor(){
      this.btn_x = Math.floor(310 + Math.random()*(1180-310));
      this.btn_y = Math.floor(Math.random()*275);
      this.posx=0; this.arrow_x=55; this.points=0;
      this.arrow = {x:this.arrow_x, y:50, w:5, h:50};
      this.btn_model = {x:this.btn_x, y:this.btn_y, w:100, h:100};
      this.pan1 = IMAGES.pan1; this.pan2 = IMAGES.pan2; this.pan_texture = this.pan1;
      this.stir_btn = {x:50, y:150, w:250, h:50};
      this.text = "Stir";
      this.dt=0;
      // audio
      this._audio_started=false;
      this.frying = new Channel();
      this.stir = new Channel();
    }
    _ensure_audio(){
      if (this._audio_started) return;
      this.frying.play(SOUNDS.frying, {loop:true, volume:0.4});
      this._audio_started = true;
    }
    getPoints(){ return this.points; }
    update(keys, mouse, dt){
      this.dt = dt; this._ensure_audio();
      // кнопка Add Fire
      if (pointInRect(mousePos, this.btn_model) && mouse.left){
        if (this.points < 240) this.points += 7;
        this.btn_x = Math.floor(310 + Math.random()*(1180-310));
        this.btn_y = Math.floor(Math.random()*275);
        this.btn_model.x=this.btn_x; this.btn_model.y=this.btn_y;
      }
      // Stir
      if (pointInRect(mousePos, this.stir_btn) && mouse.left){
        if (this.arrow_x > 56) this.pan_texture = (this.pan_texture===this.pan1)?this.pan2:this.pan1;
        this.arrow_x = 55;
        this.stir.play(SOUNDS.stir, {loop:false, volume:0.7});
      }
      if (this.arrow_x < 290) this.arrow_x += 0.5;
      if (this.arrow_x === 290){ if (this.points > 0) this.points -= 0.5; }
      if (this.points > 0) this.points -= 0.1;
      this.arrow.x = this.arrow_x; this.arrow.y = 50;
    }
    draw(g){
      // рамка
      g.strokeStyle = LightYellow; g.lineWidth = 2;
      g.beginPath(); g.moveTo(50,50); g.lineTo(300,50); g.moveTo(50,100); g.lineTo(300,100); g.moveTo(50,50); g.lineTo(50,100); g.moveTo(300,50); g.lineTo(300,100); g.stroke();
      g.fillStyle = LightYellow; g.fillRect(55,55, this.points, 40);
      g.fillStyle = "red"; g.fillRect(this.arrow.x, this.arrow.y, this.arrow.w, this.arrow.h);
      // stir btn
      g.fillStyle = LightYellow; g.fillRect(this.stir_btn.x,this.stir_btn.y,this.stir_btn.w,this.stir_btn.h);
      g.fillStyle = DarkPurple; g.font = "30px EpilepsySans"; g.textAlign="center"; g.textBaseline="middle";
      g.fillText(this.text, this.stir_btn.x + this.stir_btn.w/2, this.stir_btn.y + this.stir_btn.h/2);
      // пан + add_fire
      if (this.pan_texture) g.drawImage(this.pan_texture, 0,0, W,H);
      if (IMAGES.add_fire) g.drawImage(IMAGES.add_fire, this.btn_model.x, this.btn_model.y, this.btn_model.w, this.btn_model.h);
    }
    stop_audio(){ this.frying.stop(); }
  }

  function pointInRect(p, r){ return p.x>=r.x && p.y>=r.y && p.x<=r.x+r.w && p.y<=r.y+r.h; }

  // --- Game controller (main loop) ---------------------------------------
  let state = "menu";
  let debug = false;
  const fishing = new Fishing();
  const driving = new Driving();
  const cooking = new Cooking();

  // click handling for menu (мышь)
  canvas.addEventListener('mousedown', (e)=>{
    if (state==='menu'){
      if (pointInRect(mousePos, play_button)) {
        state='fishing';
        audio.play_music(0.1);
      }
      if (pointInRect(mousePos, quit_button)) {
        state='menu';
      }
    }
  });

  // tap handling for menu (тач)
  canvas.addEventListener('touchstart', (e) => {
    if (state !== 'menu') return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const t = e.changedTouches[0];
    const x = (t.clientX - rect.left) * scaleX;
    const y = (t.clientY - rect.top) * scaleY;
    mousePos.x = x;
    mousePos.y = y;

    if (pointInRect(mousePos, play_button)) {
      state = 'fishing';
      audio.play_music(0.1);
    } else if (pointInRect(mousePos, quit_button)) {
      state = 'menu';
    }
    e.preventDefault();
  }, { passive:false });

  let last = nowMs();
  function frame(){
    const t = nowMs();
    const dt = (t - last); // миллисекунды, как в pygame.Clock().tick()
    last = t;

    // sync touch -> keys/mouse
    const k = {
      w: keys.w || controls.key_w,
      a: keys.a || controls.key_a,
      s: keys.s || controls.key_s,
      d: keys.d || controls.key_d
    };
    const m = {
      left: mouseButtons.left || controls.mouse_left,
      right: mouseButtons.right || controls.mouse_right
    };

    // clear
    ctx.fillStyle = DarkPurple; ctx.fillRect(0,0,W,H);

    if (state==='menu'){
      play_button.draw(ctx, LightYellow);
      quit_button.draw(ctx, LightYellow);
    } else if (state==='fishing'){
      fishing.keybinds(m);
      fishing.force_draw(ctx);
      if (fishing.isFishing){
        fishing.random();
        fishing.draw(ctx);
        fishing.update(k, m, dt);
      }
      if (fishing.getFishes()===3) state='driving';
    } else if (state==='driving'){
      driving.draw(ctx);
      driving.random();
      driving.update(k, m, dt);
      if (driving.getPoints() > 239) {
        driving.stop_audio();
        state = 'cooking';
      }
    } else if (state==='cooking'){
      cooking.draw(ctx);
      cooking.update(k, m, dt);
      if (cooking.getPoints() > 239){
        cooking.stop_audio();
        state='menu';
      }
    }

    // draw on-screen controls
    controls.draw(ctx);

    requestAnimationFrame(frame);
  }

  // Load images then start loop
  Promise.all(toLoad.map(async ([k,src])=>{ IMAGES[k] = await loadImage(resourcePath(src)); })).then(()=>{
    fishing.player_texture = IMAGES.f1;
    driving.car_texture = IMAGES.car;
    cooking.pan1 = IMAGES.pan1;
    cooking.pan2 = IMAGES.pan2;
    cooking.pan_texture = cooking.pan1;
    requestAnimationFrame(frame);
  });

})();