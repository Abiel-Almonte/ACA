import './Home.css'

export function Home(){
  return(
  <body>
    <div class='home'>
    <section class='heading'>
      <video src={require("../video/background.mp4")} autoPlay loop muted />
      <div class='heading_content'>
        <h1>Course selection made easier.</h1>
        <h3>Powered by Large Language Models.</h3>
      </div>
    </section>
    <div class= 'page'>
      <div class= 'page_left'>
        <div class= 'columns'>
          <div class='img_wrapper'>
            <img src= {require("../imgs/ai-1.jpg")} alt=''/>
          </div>
          <div class='img_wrapper'>
            <img src={require("../imgs/ai-2.jpg")} alt=''></img>
          </div>
          <div class='img_wrapper'>
            <img src={require("../imgs/ai-3.jpg")} alt=''></img>
          </div>
        </div>
      </div>
      <div class= 'page_right'>
        <div class= 'page_content'>
          <h4>Welcome To</h4>
          <h2>Assistant College Advisior</h2>
          <p>An AI assitant that delivers a concierge experience to students selecting semester courses by providing class schedules, professor profiles, and ratings. Packeged all into one itertactive chat.</p>
          <div class= 'navigation'>
            <a href='login'> Continue</a>
            <a href='about'>Read more ...</a>
          </div>
        </div>
      </div>
    </div>
    </div>
  </body>
  )
}