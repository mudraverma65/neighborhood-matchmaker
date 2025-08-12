'use client';

import { useState } from 'react';
import styles from '../styles/HomePage.module.css';
import HotSpot from './Hotspot';
import SearchForm from './SearchForm';

const HomePage = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false); // <-- new state

  const handleSearchClick = () => {
    setIsSearchOpen(true);
  };

  const handleCloseSearch = () => {
    setIsSearchOpen(false);
  };

  const hotspots = [
    {
      id: 1,
      image: "/media/notre-dame.png",
      position: "top-left"
    },
    {
      id: 2,
      image: "/media/china-town.png", 
      position: "top-right"
    },
    {
      id: 3,
      image: "/media/garden.png", 
      position: "bottom-left"
    },
    {
      id: 4,
      image: "/media/biosphere.png",
      position: "bottom-right"
    }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.background}>
        
        {/* Floating background shapes */}
        <div className={styles.floatingShapes}>
          <div className={`${styles.floatingShape} ${styles.shape1}`}></div>
          <div className={`${styles.floatingShape} ${styles.shape2}`}></div>
          <div className={`${styles.floatingShape} ${styles.shape3}`}></div>
          <div className={`${styles.floatingShape} ${styles.shape4}`}></div>
        </div>

        {/* Montreal Hotspot Stickers */}
        {hotspots.map((hotspot) => (
          <HotSpot
            key={hotspot.id}
            hotspot={hotspot}
          />
        ))}

        {/* Central Search Button */}
        <div className={styles.centerContainer}>
          <div className={styles.titleSection}>
            <h1 className={styles.mainTitle}>Find Your</h1>
            <h1 className={styles.accentTitle}>Montreal Vibe</h1>
          </div>
          
          <button
            onClick={handleSearchClick}
            className={styles.searchButton}
          >
            <div className={styles.buttonShine}></div>
            <span className={styles.buttonContent}>
              <span className={styles.searchEmoji}>🔍</span>
              START EXPLORING
              <span className={styles.sparkleEmoji}>✨</span>
            </span>
          </button>

          <p className={styles.subtitle}>
            Discover neighborhoods that match your lifestyle
          </p>
        </div>

        {/* Decorative elements */}
        <div className={styles.decorativeElements}>
          <div className={`${styles.decorElement} ${styles.decor1}`}>🍁</div>
          <div className={`${styles.decorElement} ${styles.decor2}`}>🏔️</div>
          <div className={`${styles.decorElement} ${styles.decor3}`}>❄️</div>
        </div>

        {isSearchOpen && (
          <SearchForm isOpen={true} onClose={handleCloseSearch} />
        )}
      </div>
    </div>
  );
};

export default HomePage;