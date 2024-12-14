import React, {useState, useEffect} from 'react'
import { makeStyles } from '@material-ui/core/styles'
import Card from '@material-ui/core/Card'
import CardMedia from '@material-ui/core/CardMedia'
import CardContent from '@material-ui/core/CardContent'
import Typography from '@material-ui/core/Typography'
import inventorCircleImg from './../assets/images/inventor_circle_collaboration.jpg'
import Grid from '@material-ui/core/Grid'
import auth from './../auth/auth-helper'
import FindPeople from './../user/FindPeople'
import Newsfeed from './../post/Newsfeed'
import networkImg from './../assets/images/networking.jpg'
import { teal, orange } from '@material-ui/core/colors'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    minHeight: '100vh',
    backgroundImage: `url(${networkImg})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'repeat',
    zIndex: 1
  },
  card: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    position: 'relative',
  },
  media: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundImage: `url(${inventorCircleImg})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    zIndex: 1,
  },
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(47, 46, 46, 0.7)', // Semi-transparent overlay
    //backgroundColor: 'rgba(33, 33, 33, 0.6)',
    zIndex: 2,
  },
  textContainer: {
    position: 'relative',
    zIndex: 3, // Above the overlay
    //color: 'rgba(226, 155, 62, 0.8)',
    color: '#fff',
    top: -140,
    textAlign: 'center',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 'bold',
    marginBottom: theme.spacing(2),
  },
  subtitle: {
    fontSize: '1.5rem',
  },
}));

export default function Home({history}){
  const classes = useStyles()
  const [defaultPage, setDefaultPage] = useState(false)

  useEffect(()=> {
    setDefaultPage(auth.isAuthenticated())
    const unlisten = history.listen (() => {
      setDefaultPage(auth.isAuthenticated())
    })
    return () => {
      unlisten()
    }
  }, [])

    return (
      <div className={classes.root}>
        { !defaultPage &&
         
            <Card className={classes.card}>
              
              <div className={classes.media}></div> 
               <div className={classes.overlay}></div>
               <div className={classes.textContainer}>
          <div className={classes.title}>Welcome to Inventors Circle: A Collaborative Social Network</div>
          <div className={classes.subtitle}><p>Where innovation meets collaboration. <br></br>

Join a thriving community of inventors, mentors, and visionaries. <br></br>Discover the resources, connections, and inspiration you need to transform your ideas into reality.</p></div>
          <div className={classes.subtitle}><b>Innovate, Collaborate, Achieve</b></div>
        </div>
               
            </Card>
           
        }
        {defaultPage &&
        
          <Grid container spacing={8}>
            <Grid item xs={8} sm={7}>
           
              <Newsfeed/>
             
            </Grid>
            <Grid item xs={6} sm={5}>
           
              <FindPeople/>
            </Grid>
          </Grid>
        }
      </div>
    )
}
