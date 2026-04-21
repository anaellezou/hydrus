import { useState, useEffect, useCallback, useRef } from "react";
import styled, { createGlobalStyle, keyframes, css } from "styled-components";

// ─── Config ────────────────────────────────────────────────────────────────
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5001/api";
const LEVELS = ["N5", "N4", "N3", "N2", "N1"];
const SECTIONS = ["vocabulary", "kanji", "grammar"];
const DROPDOWN_OFFSET_X = 110;
const MOBILE_BREAKPOINT = 768;

// ─── Global Styles ──────────────────────────────────────────────────────────
const GlobalStyle = createGlobalStyle`
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Montserrat:wght@200;300;400&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:          #0a0c0f;
    --glass:       rgba(10, 12, 15, 0.72);
    --glass-light: rgba(255, 255, 255, 0.04);
    --border:      rgba(255, 255, 255, 0.08);
    --white:       #f0ede8;
    --muted:       rgba(240, 237, 232, 0.45);
    --accent:      rgba(200, 210, 220, 0.9);
    --kanji-size:  clamp(2.8rem, 6vw, 5rem);
  }

  html, body, #root {
    min-height: 100%;
    width: 100%;
    overflow: auto;
  }

  body {
    font-family: 'Montserrat', sans-serif;
    font-weight: 300;
    background: var(--bg);
    color: var(--white);
    letter-spacing: 0.04em;
  }

  ::-webkit-scrollbar { width: 2px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
`;

// ─── Animations ─────────────────────────────────────────────────────────────
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
`;
const slideDown = keyframes`
  from { opacity: 0; transform: translateX(-50%) translateY(-8px); }
  to   { opacity: 1; transform: translateX(-50%) translateY(0); }
`;
const shimmer = keyframes`
  0%,100% { opacity: 0.4; }
  50%      { opacity: 0.7; }
`;
const slideInLeft = keyframes`
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
`;
const expandSection = keyframes`
  from { opacity: 0; max-height: 0; }
  to   { opacity: 1; max-height: 200px; }
`;

// ─── Layout ─────────────────────────────────────────────────────────────────
const Root = styled.div`
  position: relative;
  min-height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
`;

const BgImage = styled.div`
  position: fixed;
  inset: 0;
  background: url('/background.jpg') center/cover no-repeat;
  filter: brightness(0.38) saturate(0.7);
  z-index: 0;
`;

const BgOverlay = styled.div`
  position: fixed;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(5, 8, 14, 0.55) 0%,
    rgba(10, 14, 20, 0.3) 50%,
    rgba(5, 8, 14, 0.7) 100%
  );
  z-index: 1;
`;

// ─── Desktop Header ──────────────────────────────────────────────────────────
const Header = styled.header`
  position: relative;
  z-index: 30;
  display: flex;
  align-items: center;
  gap: 2.5rem;
  padding: 2rem 3rem;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    display: none;
  }
`;

const MaskImage = styled.img`
  width: 152px;
  height: 152px;
  object-fit: contain;
  filter: contrast(1.1) brightness(0.95);
  opacity: 0.88;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
`;

const LevelTabs = styled.nav`
  display: flex;
  gap: 1rem;
  position: relative;
  z-index: 31;
`;

const LevelBtn = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 200;
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  color: ${({ $active }) => ($active ? "var(--white)" : "var(--muted)")};
  padding: 0.55rem 1.1rem;
  position: relative;
  transition: color 0.2s ease;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: ${({ $active }) => ($active ? "100%" : "0")};
    height: 1px;
    background: var(--white);
    transition: width 0.25s ease;
  }

  &:hover { color: var(--white); }
`;

const AppTitle = styled.h1`
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-size: 1.1rem;
  letter-spacing: 0.35em;
  color: var(--muted);
  margin-left: auto;
  text-transform: uppercase;
`;

// ─── Desktop Dropdown ────────────────────────────────────────────────────────
const DropdownWrap = styled.div`
  position: fixed;
  top: ${({ $top }) => $top}px;
  left: ${({ $left }) => $left}px;
  transform: translateX(-50%);
  z-index: 40;
  pointer-events: auto;
  display: flex;
  gap: 0.8rem;
  animation: ${slideDown} 0.3s ease forwards;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    display: none;
  }
`;

const SectionBtn = styled.button`
  background: ${({ $active }) => ($active ? "rgba(255,255,255,0.09)" : "transparent")};
  border: 1px solid ${({ $active }) => ($active ? "rgba(255,255,255,0.18)" : "var(--border)")};
  border-radius: 2px;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 200;
  font-size: 0.65rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: ${({ $active }) => ($active ? "var(--white)" : "var(--muted)")};
  padding: 0.5rem 1.4rem;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255,255,255,0.06);
    color: var(--white);
    border-color: rgba(255,255,255,0.2);
  }
`;

// ─── Mobile Header ───────────────────────────────────────────────────────────
const MobileHeader = styled.header`
  display: none;
  position: relative;
  z-index: 30;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1.5rem 1rem;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    display: flex;
  }
`;

const MobileMaskImage = styled.img`
  width: 100px;
  height: 100px;
  object-fit: contain;
  filter: contrast(1.1) brightness(0.95);
  opacity: 0.88;
  margin-bottom: 0.5rem;
`;

const MobileAppTitle = styled.h1`
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-size: 0.9rem;
  letter-spacing: 0.35em;
  color: var(--muted);
  text-transform: uppercase;
`;

// ─── Mobile Toaster Menu ─────────────────────────────────────────────────────
const ToasterBtn = styled.button`
  position: fixed;
  top: 1.5rem;
  left: 1.5rem;
  z-index: 50;
  background: rgba(10, 12, 15, 0.85);
  border: 1px solid var(--border);
  border-radius: 3px;
  width: 40px;
  height: 40px;
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
  backdrop-filter: blur(12px);
  transition: border-color 0.2s ease;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    display: flex;
  }

  &:hover {
    border-color: rgba(255,255,255,0.2);
  }
`;

const ToasterLine = styled.span`
  display: block;
  width: 16px;
  height: 1px;
  background: var(--white);
  transition: all 0.25s ease;
  transform-origin: center;

  &:nth-child(1) {
    transform: ${({ $open }) => $open ? "translateY(6px) rotate(45deg)" : "none"};
  }
  &:nth-child(2) {
    opacity: ${({ $open }) => $open ? "0" : "1"};
  }
  &:nth-child(3) {
    transform: ${({ $open }) => $open ? "translateY(-6px) rotate(-45deg)" : "none"};
  }
`;

const MobileMenuOverlay = styled.div`
  display: none;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 45;
    background: transparent;
    pointer-events: ${({ $open }) => $open ? "auto" : "none"};
  }
`;

const MobileMenuPanel = styled.div`
  display: none;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 220px;
    z-index: 46;
    background: rgba(8, 10, 13, 0.96);
    border-right: 1px solid var(--border);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    transform: ${({ $open }) => $open ? "translateX(0)" : "translateX(-100%)"};
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 5rem 0 2rem;
    overflow-y: auto;
  }
`;

const MobileLevelItem = styled.div`
  border-bottom: 1px solid var(--border);
`;

const MobileLevelBtn = styled.button`
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 200;
  font-size: 0.72rem;
  letter-spacing: 0.22em;
  color: ${({ $active }) => ($active ? "var(--white)" : "var(--muted)")};
  padding: 1.1rem 1.8rem;
  text-align: left;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: color 0.2s ease, background 0.2s ease;

  &:hover {
    color: var(--white);
    background: rgba(255,255,255,0.03);
  }

  &::after {
    content: '';
    display: block;
    width: 5px;
    height: 5px;
    border-right: 1px solid currentColor;
    border-bottom: 1px solid currentColor;
    transform: ${({ $active }) => $active ? "rotate(-135deg)" : "rotate(45deg)"};
    transition: transform 0.25s ease;
    opacity: 0.5;
  }
`;

const MobileSectionsWrap = styled.div`
  overflow: hidden;
  max-height: ${({ $open }) => $open ? "200px" : "0"};
  transition: max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
`;

const MobileSectionBtn = styled.button`
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 200;
  font-size: 0.6rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: ${({ $active }) => ($active ? "var(--white)" : "var(--muted)")};
  padding: 0.8rem 1.8rem 0.8rem 2.8rem;
  text-align: left;
  transition: color 0.2s ease, background 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.6rem;

  &::before {
    content: '';
    display: block;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: ${({ $active }) => ($active ? "var(--white)" : "var(--muted)")};
    flex-shrink: 0;
    transition: background 0.2s ease;
  }

  &:hover {
    color: var(--white);
    background: rgba(255,255,255,0.03);
    &::before { background: var(--white); }
  }
`;

// ─── Content Panel ───────────────────────────────────────────────────────────
const ContentArea = styled.main`
  position: relative;
  z-index: 5;
  flex: 1;
  padding: 1.8rem 3rem 4rem;
  margin-top: 1rem;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    padding: 1rem 1rem 3rem;
    margin-top: 0;
  }
`;

const Panel = styled.div`
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 4px;
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);
  padding: 2.5rem 3rem;
  animation: ${fadeIn} 0.35s ease;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    padding: 1.5rem 1.2rem;
  }
`;

const LoadingText = styled.p`
  color: var(--muted);
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  animation: ${shimmer} 1.8s ease infinite;
`;

const EmptyText = styled.p`
  color: var(--muted);
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
`;

// ─── Filter Bar ──────────────────────────────────────────────────────────────
const FilterBar = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2.2rem;
  padding-bottom: 1.5rem;
  padding-top: 1rem;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(10, 12, 15, 0.98);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  margin-left: -3rem;
  margin-right: -3rem;
  padding-left: 3rem;
  padding-right: 3rem;

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    margin-left: -1.2rem;
    margin-right: -1.2rem;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
  }
`;

const FilterChip = styled.button`
  background: ${({ $active }) => ($active ? "rgba(255,255,255,0.1)" : "transparent")};
  border: 1px solid ${({ $active }) => ($active ? "rgba(255,255,255,0.25)" : "var(--border)")};
  border-radius: 2px;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 200;
  font-size: 0.58rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: ${({ $active }) => ($active ? "var(--white)" : "var(--muted)")};
  padding: 0.35rem 0.9rem;
  transition: all 0.18s ease;

  &:hover {
    border-color: rgba(255,255,255,0.2);
    color: var(--white);
  }
`;

// ─── Grid & Cards ────────────────────────────────────────────────────────────
const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }
`;

const Card = styled.div`
  background: var(--glass);
  padding: 1.8rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  cursor: default;
  transition: background 0.2s ease;
  animation: ${fadeIn} 0.4s ease both;
  animation-delay: ${({ $index }) => Math.min($index * 0.015, 0.3)}s;

  &:hover { background: rgba(255,255,255,0.045); }

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    padding: 1.2rem 1rem;
  }
`;

const CardMain = styled.span`
  font-family: 'Cormorant Garamond', serif;
  font-size: var(--kanji-size);
  font-weight: 400;
  line-height: 1;
  color: var(--white);
  letter-spacing: 0.02em;
`;

const CardReading = styled.span`
  font-size: 0.62rem;
  font-weight: 200;
  letter-spacing: 0.15em;
  color: var(--accent);
`;

const CardMeaning = styled.span`
  font-size: 0.68rem;
  font-weight: 300;
  color: var(--muted);
  letter-spacing: 0.08em;
  line-height: 1.5;
`;

const CardType = styled.span`
  font-size: 0.55rem;
  font-weight: 200;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.25);
  margin-top: 0.2rem;
`;

// ─── Grammar List ────────────────────────────────────────────────────────────
const GrammarList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
`;

const GrammarRow = styled.div`
  background: var(--glass);
  padding: 1.4rem 2rem;
  display: grid;
  grid-template-columns: 220px 1fr 2fr;
  align-items: center;
  gap: 2rem;
  transition: background 0.2s ease;
  animation: ${fadeIn} 0.4s ease both;
  animation-delay: ${({ $index }) => Math.min($index * 0.012, 0.3)}s;

  &:hover { background: rgba(255,255,255,0.04); }

  @media (max-width: ${MOBILE_BREAKPOINT}px) {
    grid-template-columns: 1fr;
    gap: 0.4rem;
    padding: 1rem 1.2rem;
  }
`;

const GrammarRomaji = styled.span`
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--white);
  letter-spacing: 0.05em;
`;

const GrammarJP = styled.span`
  font-size: 1.1rem;
  color: var(--accent);
  letter-spacing: 0.1em;
`;

const GrammarMeaning = styled.span`
  font-size: 0.68rem;
  color: var(--muted);
  letter-spacing: 0.1em;
  line-height: 1.5;
`;

// ─── Helpers ─────────────────────────────────────────────────────────────────
function getVocabTypes(items) {
  const types = new Set();
  items.forEach(item => {
    if (item.type) {
      const primary = item.type.split(",")[0].trim();
      types.add(primary);
    }
  });
  return ["All", ...Array.from(types).sort()];
}

function truncateMeaning(str, max = 48) {
  if (!str) return "";
  return str.length > max ? str.slice(0, max) + "…" : str;
}

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= MOBILE_BREAKPOINT);
  useEffect(() => {
    const handler = () => setIsMobile(window.innerWidth <= MOBILE_BREAKPOINT);
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, []);
  return isMobile;
}

// ─── Sub-views ───────────────────────────────────────────────────────────────
function KanjiView({ level }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/kanji/?level=${level}`)
      .then(r => r.json())
      .then(d => { setItems(d.kanji || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [level]);

  if (loading) return <LoadingText>Loading kanji…</LoadingText>;
  if (!items.length) return <EmptyText>No kanji for {level} yet.</EmptyText>;

  return (
    <Grid>
      {items.map((k, i) => (
        <Card key={k.id} $index={i}>
          <CardMain>{k.kanji}</CardMain>
          <CardReading>{k.onReading && `音  ${k.onReading}`}</CardReading>
          <CardReading>{k.kunReading && `訓  ${k.kunReading}`}</CardReading>
          <CardMeaning>{truncateMeaning(k.meaning)}</CardMeaning>
        </Card>
      ))}
    </Grid>
  );
}

function VocabularyView({ level }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [types, setTypes] = useState(["All"]);
  const [activeType, setActiveType] = useState("All");

  useEffect(() => {
    setLoading(true);
    setActiveType("All");
    fetch(`${API_BASE}/vocabulary/?level=${level}`)
      .then(r => r.json())
      .then(d => {
        const vocab = d.vocabulary || [];
        setItems(vocab);
        setTypes(getVocabTypes(vocab));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [level]);

  const filtered = activeType === "All"
    ? items
    : items.filter(v => v.type && v.type.startsWith(activeType));

  if (loading) return <LoadingText>Loading vocabulary…</LoadingText>;
  if (!items.length) return <EmptyText>No vocabulary for {level} yet.</EmptyText>;

  return (
    <>
      <FilterBar>
        {types.map(t => (
          <FilterChip key={t} $active={activeType === t} onClick={() => setActiveType(t)}>
            {t}
          </FilterChip>
        ))}
      </FilterBar>
      <Grid>
        {filtered.map((v, i) => (
          <Card key={v.id} $index={i}>
            <CardMain>{v.vocab}</CardMain>
            {v.reading?.hiragana && <CardReading>{v.reading.hiragana}</CardReading>}
            {v.reading?.romaji && <CardReading style={{ opacity: 0.5 }}>{v.reading.romaji}</CardReading>}
            <CardMeaning>{truncateMeaning(v.meaning)}</CardMeaning>
            {v.type && <CardType>{v.type.split(",")[0]}</CardType>}
          </Card>
        ))}
      </Grid>
    </>
  );
}

function GrammarView({ level }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/grammar/?level=${level}`)
      .then(r => r.json())
      .then(d => { setItems(d.grammar || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [level]);

  if (loading) return <LoadingText>Loading grammar…</LoadingText>;
  if (!items.length) return <EmptyText>No grammar for {level} yet.</EmptyText>;

  return (
    <GrammarList>
      {items.map((g, i) => (
        <GrammarRow key={g.id} $index={i}>
          <GrammarRomaji>{g.romaji}</GrammarRomaji>
          <GrammarJP>{g.japanese}</GrammarJP>
          <GrammarMeaning>{g.meaning}</GrammarMeaning>
        </GrammarRow>
      ))}
    </GrammarList>
  );
}

// ─── App ─────────────────────────────────────────────────────────────────────
export default function App() {
  const isMobile = useIsMobile();

  // Desktop state
  const [activeLevel, setActiveLevel] = useState(null);
  const [activeSection, setActiveSection] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const [dropdownPos, setDropdownPos] = useState({ top: 0, left: 0 });

  // Mobile state
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [mobileExpandedLevel, setMobileExpandedLevel] = useState(null);

  // ── Desktop handlers ──
  const handleLevelClick = useCallback((level, e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setDropdownPos({
      top: rect.bottom + 12,
      left: rect.left + rect.width / 2 + DROPDOWN_OFFSET_X,
    });
    if (activeLevel === level && showDropdown) {
      setShowDropdown(false);
    } else {
      setActiveLevel(level);
      setShowDropdown(true);
      setActiveSection(null);
    }
  }, [activeLevel, showDropdown]);

  const handleSectionClick = useCallback((section) => {
    setActiveSection(section);
    setShowDropdown(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  // ── Mobile handlers ──
  const handleMobileLevelClick = useCallback((level) => {
    setMobileExpandedLevel(prev => prev === level ? null : level);
  }, []);

  const handleMobileSectionClick = useCallback((level, section) => {
    setActiveLevel(level);
    setActiveSection(section);
    setMobileMenuOpen(false);
    setMobileExpandedLevel(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  return (
    <>
      <GlobalStyle />
      <Root>
        <BgImage />
        <BgOverlay />

        {/* ── Desktop Header ── */}
        <Header>
          <MaskImage src="/mask.png" alt="mask" />
          <LevelTabs>
            {LEVELS.map(level => (
              <LevelBtn
                key={level}
                $active={activeLevel === level}
                onClick={(e) => handleLevelClick(level, e)}
              >
                {level}
              </LevelBtn>
            ))}
          </LevelTabs>
          <AppTitle>水蛇座 · Hydrus</AppTitle>
        </Header>

        {/* ── Desktop Dropdown ── */}
        {showDropdown && !isMobile && (
          <DropdownWrap
            key={activeLevel}
            $top={dropdownPos.top}
            $left={dropdownPos.left}
          >
            {SECTIONS.map(section => (
              <SectionBtn
                key={section}
                $active={activeSection === section}
                onClick={() => handleSectionClick(section)}
              >
                {section}
              </SectionBtn>
            ))}
          </DropdownWrap>
        )}

        {/* ── Mobile Header ── */}
        <MobileHeader>
          <MobileMaskImage src="/mask.png" alt="mask" />
          <MobileAppTitle>水蛇座 · Hydrus</MobileAppTitle>
        </MobileHeader>

        {/* ── Mobile Toaster Button ── */}
        <ToasterBtn onClick={() => setMobileMenuOpen(o => !o)} aria-label="Menu">
          <ToasterLine $open={mobileMenuOpen} />
          <ToasterLine $open={mobileMenuOpen} />
          <ToasterLine $open={mobileMenuOpen} />
        </ToasterBtn>

        {/* ── Mobile Menu Overlay (close on tap outside) ── */}
        <MobileMenuOverlay
          $open={mobileMenuOpen}
          onClick={() => setMobileMenuOpen(false)}
        />

        {/* ── Mobile Slide-in Panel ── */}
        <MobileMenuPanel $open={mobileMenuOpen}>
          {LEVELS.map(level => (
            <MobileLevelItem key={level}>
              <MobileLevelBtn
                $active={mobileExpandedLevel === level}
                onClick={() => handleMobileLevelClick(level)}
              >
                {level}
              </MobileLevelBtn>
              <MobileSectionsWrap $open={mobileExpandedLevel === level}>
                {SECTIONS.map(section => (
                  <MobileSectionBtn
                    key={section}
                    $active={activeLevel === level && activeSection === section}
                    onClick={() => handleMobileSectionClick(level, section)}
                  >
                    {section}
                  </MobileSectionBtn>
                ))}
              </MobileSectionsWrap>
            </MobileLevelItem>
          ))}
        </MobileMenuPanel>

        {/* ── Content ── */}
        {activeLevel && activeSection && (
          <ContentArea>
            <Panel key={`${activeLevel}-${activeSection}`}>
              {activeSection === "kanji" && <KanjiView level={activeLevel} />}
              {activeSection === "vocabulary" && <VocabularyView level={activeLevel} />}
              {activeSection === "grammar" && <GrammarView level={activeLevel} />}
            </Panel>
          </ContentArea>
        )}
      </Root>
    </>
  );
}