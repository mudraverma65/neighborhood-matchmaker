// 'use client';

// import { useRouter } from 'next/navigation';
// import { useEffect, useState } from 'react';
// import { useSearch } from '../contexts/SearchContext';
// import NeighborhoodCard from './NeighborhoodCard';
// import PodiumCard from './PodiumCard';
// import styles from './Results.module.css';

// const Results = () => {
//   const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
//   const [searchCriteria, setSearchCriteria] = useState<NeighborhoodSearchDTO | null>(null);
//   const [loading, setLoading] = useState(true);
//   const router = useRouter();

//   useEffect(() => {
//     // Read data from localStorage
//     const savedResults = localStorage.getItem('searchResults');
//     const savedCriteria = localStorage.getItem('searchCriteria');
    
//     if (savedResults) {
//       try {
//         const parsedResults: SearchResult = JSON.parse(savedResults);
//         setSearchResults(parsedResults);
        
//         if (savedCriteria) {
//           const parsedCriteria: NeighborhoodSearchDTO = JSON.parse(savedCriteria);
//           setSearchCriteria(parsedCriteria);
//         }
//       } catch (error) {
//         console.error('Error parsing saved results:', error);
//         router.push('/');
//       }
//     } else {
//       // No results found, redirect back to search
//       router.push('/');
//     }
    
//     setLoading(false);
//   }, [router]);

//   const handleBackToSearch = () => {
//     router.push('/');
//   };

//   const handleNewSearch = () => {
//     // Clear stored results for a fresh search
//     localStorage.removeItem('searchResults');
//     localStorage.removeItem('searchCriteria');
//     router.push('/');
//   };

//   if (loading) {
//     return (
//       <div className={styles.container}>
//         <div className={styles.loadingContainer}>
//           <div className={styles.spinner}></div>
//           <h2 className={styles.loadingText}>Finding your perfect neighborhoods...</h2>
//           <p className={styles.loadingSubtext}>✨ Analyzing amenities and locations ✨</p>
//         </div>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className={styles.container}>
//         <div className={styles.errorContainer}>
//           <div className={styles.errorIcon}>😔</div>
//           <h2 className={styles.errorTitle}>Oops! Something went wrong</h2>
//           <p className={styles.errorMessage}>{error}</p>
//           <button className={styles.retryButton} onClick={handleBackToSearch}>
//             Back to Search
//           </button>
//         </div>
//       </div>
//     );
//   }

//   if (!results || results.neighborhoods.length === 0) {
//     return (
//       <div className={styles.container}>
//         <div className={styles.noResultsContainer}>
//           <div className={styles.noResultsIcon}>🔍</div>
//           <h2 className={styles.noResultsTitle}>No neighborhoods found</h2>
//           <p className={styles.noResultsMessage}>
//             Try adjusting your search criteria to find more options
//           </p>
//           <button className={styles.newSearchButton} onClick={handleNewSearch}>
//             New Search
//           </button>
//         </div>
//       </div>
//     );
//   }

//   const topThree = results.neighborhoods.slice(0, 3);
//   const remaining = results.neighborhoods.slice(3);

//   return (
//     <div className={styles.container}>
//       <div className={styles.header}>
//         <button className={styles.backButton} onClick={handleBackToSearch}>
//           ← Back to Search
//         </button>
//         <div className={styles.headerContent}>
//           <h1 className={styles.title}>Your Perfect Montreal Neighborhoods</h1>
//           <p className={styles.subtitle}>
//             Found {results.total_results} neighborhoods matching your criteria
//           </p>
//         </div>
//       </div>

//       {/* Top 3 Podium */}
//       <div className={styles.podiumSection}>
//         <h2 className={styles.podiumTitle}>🏆 Top Picks</h2>
//         <div className={styles.podium}>
//           {topThree.map((neighborhood, index) => (
//             <PodiumCard
//               key={neighborhood.neighborhood_id}
//               neighborhood={neighborhood}
//               position={index + 1}
//               rank={index + 1}
//             />
//           ))}
//         </div>
//       </div>

//       {/* Remaining Neighborhoods */}
//       {remaining.length > 0 && (
//         <div className={styles.otherResultsSection}>
//           <h2 className={styles.otherResultsTitle}>Other Great Options</h2>
//           <div className={styles.neighborhoodGrid}>
//             {remaining.map((neighborhood, index) => (
//               <NeighborhoodCard
//                 key={neighborhood.neighborhood_id}
//                 neighborhood={neighborhood}
//                 rank={index + 4}
//               />
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Search Criteria Summary */}
//       <div className={styles.searchSummary}>
//         <h3 className={styles.summaryTitle}>Search Criteria</h3>
//         <div className={styles.criteriaGrid}>
//           {results.search_criteria.budget && (
//             <div className={styles.criteriaItem}>
//               <span className={styles.criteriaIcon}>💰</span>
//               <span className={styles.criteriaLabel}>Budget:</span>
//               <span className={styles.criteriaValue}>${results.search_criteria.budget}/month</span>
//             </div>
//           )}
//           {results.search_criteria.max_commute_time && (
//             <div className={styles.criteriaItem}>
//               <span className={styles.criteriaIcon}>🚇</span>
//               <span className={styles.criteriaLabel}>Max Commute:</span>
//               <span className={styles.criteriaValue}>{results.search_criteria.max_commute_time} min</span>
//             </div>
//           )}
//           {results.search_criteria.amenities && results.search_criteria.amenities.length > 0 && (
//             <div className={styles.criteriaItem}>
//               <span className={styles.criteriaIcon}>🎯</span>
//               <span className={styles.criteriaLabel}>Amenities:</span>
//               <span className={styles.criteriaValue}>{results.search_criteria.amenities.length} selected</span>
//             </div>
//           )}
//         </div>
//       </div>

//       <div className={styles.actions}>
//         <button className={styles.newSearchButton} onClick={handleNewSearch}>
//           🔍 New Search
//         </button>
//       </div>
//     </div>
//   );
// };

// export default Results;
