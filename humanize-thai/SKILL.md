---
name: humanize-thai
description: |
  Rewrite Thai text that sounds AI-generated so it reads like a Thai writer,
  without changing what it says. Use when editing, reviewing, or polishing Thai
  prose for translationese, inflated claims, tourism-brochure language, การ/ความ
  nominalization, ถูก-passive overuse, ซึ่ง-chaining, connector pileup, redundant
  doublets, vague sources, chatbot leftovers, or wrong register and particles.
  Also use as a final style pass on Thai output produced by another skill.
license: MIT
---

# Humanize Thai: remove AI writing patterns from Thai prose

Rewrite Thai text that sounds AI-generated so it reads like a Thai person wrote it. Do not change what it says or invent details.

The core problem in AI-written Thai is not word choice. It is **English sentence structure wrapped in Thai words**. Each sentence is grammatical, but Thai speakers do not build sentences that way. The main job of this skill is to dismantle that structure and rewrite to the rhythm of Thai.

## What to do

1. **Find the patterns.** Check the text against the patterns below.
2. **Keep every claim.** You may shorten dull parts, expand useful parts, and merge or split paragraphs. Keep the information even when you change the structure.
3. **Do not invent facts.** Do not add a name, number, date, quote, or citation unless it comes from the source or the user. If a sentence needs a missing detail, ask for it or write a shorter sentence. You may add an opinion or reaction when the voice calls for it, but never a factual claim. Fiction is exempt.
4. **Keep the original register.** Do not push casual text into bureaucratic Thai, and do not push an official document into spoken Thai.

The input type controls what you return. See [How to return the result](#how-to-return-the-result). Every mode uses the same rewrite process.

## Match the writer's voice first

If the user provides a writing sample of their own, analyze it before rewriting.

1. Read the sample first. Note sentence length, spacing habits, favorite connectors, sentence-final particles, how much English they mix in, and words they repeat.
2. Write to those habits. Do not convert their spoken words into written forms, and do not remove their personal quirks.
3. If there is no sample, use the guidance below.

**A writing sample outranks every rule in this file.** If they use อีกทั้ง often, or space their text densely, match their rate. Do not apply §7 or §14 as a ban.

## Register and sentence-final particles

Thai separates register more sharply than English. Pick the level that fits the job, then hold it across the whole piece.

- **Formal — documents, manuals, official text.** No ครับ/ค่ะ. No first-person pronouns. Plain declarative sentences.
- **Semi-formal — articles, README, blog.** Few pronouns. No particles, or only in the opening and closing paragraph.
- **Conversational — chat, posts, replies.** Particles and mood words are normal. Use them freely.

The most common register failure in AI Thai is **particles where they do not belong**, such as a technical document ending every sentence with ครับ, or **switching between ครับ and ค่ะ mid-document**. Pick one and hold it. Do not sprinkle a particle on every sentence either; Thai writers use them in bursts, not on every line.

Pronouns work the same way. Pick ผม, ดิฉัน, เรา, or no pronoun at all, and do not switch.

## Keep technical terms in English

Keep technical terms in their original English form. Do not translate them into Thai, transliterate them into Thai script, invent Thai equivalents, or append a parenthetical Thai gloss. This covers identifiers, file paths, API names, commands, package names, framework names, and established software vocabulary such as deploy, endpoint, cache, middleware, branch, commit, queue, worker, and token.

Write the surrounding sentence in natural Thai and drop the term in unchanged.

**Before:**
> ระบบจะทำการลองใหม่ (retry) สำหรับงานที่ล้มเหลว (failed) ผ่านคิวงาน (queue) เดิม
**After:**
> ระบบจะ retry งานที่ fail ผ่าน queue เดิม

When readers may not know a term, keep the term and explain what it does in a separate clause. Do not substitute a Thai word for it. Write "middleware จะตรวจ request ก่อนส่งต่อไปยัง handler หลัก", not "middleware (ตัวกลาง)".

Loanwords that have fully entered Thai are the exception: คอมพิวเตอร์, อินเทอร์เน็ต, ไฟล์, เมนู, แอป are ordinary Thai words. Write them in Thai.

---

## Group 1: Content patterns

### 1. Inflated claims about importance

**Words to watch:** ถือเป็น, นับเป็น, หมุดหมายสำคัญ, ก้าวสำคัญ, จุดเปลี่ยนครั้งสำคัญ, มีบทบาทสำคัญอย่างยิ่ง, สะท้อนให้เห็นถึง, ตอกย้ำถึง, อย่างแท้จริง, อย่างมีนัยสำคัญ, ปูทางไปสู่, หยั่งรากลึก, ทิ้งร่องรอยเอาไว้, ในภาพที่กว้างขึ้น, ท่ามกลางยุคสมัยที่เปลี่ยนแปลง, ความมุ่งมั่น

**Problem:** AI Thai claims that ordinary details are a major turning point or reflect a national trend.

**Before:**
> การก่อตั้งสถาบันวิจัยแห่งนี้ในปี 2532 ถือเป็นหมุดหมายสำคัญที่สะท้อนให้เห็นถึงวิวัฒนาการอันยาวนานของวงการวิจัยไทย และตอกย้ำถึงความมุ่งมั่นอย่างแท้จริงในการยกระดับองค์ความรู้ของประเทศ
**After:**
> สถาบันวิจัยแห่งนี้ก่อตั้งในปี 2532 เป็นส่วนหนึ่งของการกระจายงานวิจัยออกจากส่วนกลาง

### 2. Name-dropping to prove importance

**Words to watch:** สื่อชั้นนำทั้งในและต่างประเทศ, ได้รับการกล่าวถึงอย่างกว้างขวาง, ผู้ติดตามกว่า, เป็นที่ยอมรับในระดับสากล, ผู้เชี่ยวชาญชั้นนำ

**Problem:** Listing outlets or follower counts to prove someone matters, without saying what they said.

**Before:**
> ผลงานของเธอได้รับการกล่าวถึงในสื่อชั้นนำทั้งในและต่างประเทศ ไม่ว่าจะเป็น BBC, The New York Times, Financial Times และสื่อท้องถิ่นอีกหลายสำนัก อีกทั้งยังมีผู้ติดตามบนโซเชียลมีเดียกว่า 500,000 คน
**After:**
> BBC และ The New York Times เคยอ้างอิงความเห็นของเธอ

If the source says what she said and where, keep that. Do not invent context to justify a shorter version.

### 3. Empty ซึ่ง / อันเป็นการ clauses

**Words to watch:** ซึ่งสะท้อนถึง, อันเป็นการตอกย้ำ, ส่งผลให้เกิด, ก่อให้เกิด, นำไปสู่, อันแสดงให้เห็นถึง, ซึ่งสอดคล้องกับ, โดยมุ่งหวังให้เกิด

**Problem:** A trailing clause bolted onto a plain fact to make it sound profound, adding nothing. This is the Thai equivalent of the English shallow `-ing` phrase.

**Before:**
> วัดแห่งนี้ใช้โทนสีน้ำเงิน เขียว และทอง ซึ่งสอดคล้องกับความงามของธรรมชาติในท้องถิ่น อันเป็นการสะท้อนถึงความผูกพันอันลึกซึ้งระหว่างชุมชนกับผืนแผ่นดิน
**After:**
> วัดแห่งนี้ทาสีน้ำเงิน เขียว และทอง ตามสีของทะเลและทุ่งนาในพื้นที่

### 4. Tourism-brochure and sales language

**Words to watch:** ตั้งตระหง่าน, ตั้งอยู่ใจกลาง, ท่ามกลาง, เปี่ยมด้วย, อุดมไปด้วย, มนต์เสน่ห์, อันทรงคุณค่า, ตราตรึงใจ, งดงามราวกับ, ห้ามพลาด, สุดอลังการ, เลื่องชื่อ, ระดับตำนาน, ครบครัน, ตอบโจทย์ทุกไลฟ์สไตล์, ยกระดับประสบการณ์, พลิกโฉม, ไร้รอยต่อ, ครบวงจร

**Problem:** Reads like an advertisement. Common when describing places, culture, products, or organizations.

**Before:**
> ท่ามกลางขุนเขาอันเขียวขจีของจังหวัดน่าน อำเภอปัวตั้งตระหง่านเป็นเมืองเล็ก ๆ ที่เปี่ยมด้วยมนต์เสน่ห์ อุดมไปด้วยวัฒนธรรมอันทรงคุณค่าและธรรมชาติที่งดงามตราตรึงใจ
**After:**
> ปัวเป็นอำเภอหนึ่งในจังหวัดน่าน อยู่ในหุบเขา มีชุมชนไทลื้อและแหล่งทอผ้าเก่าแก่

Only keep ไทลื้อ and ทอผ้า if the source supplies them. Otherwise stop after the first clause.

### 5. Vague sources

**Words to watch:** ผู้เชี่ยวชาญระบุว่า, นักวิเคราะห์มองว่า, หลายฝ่ายเห็นตรงกันว่า, มีรายงานว่า, แหล่งข่าวเผยว่า, เป็นที่ทราบกันดีว่า, จากข้อมูลที่มีอยู่, นักวิชาการหลายท่าน

**Problem:** Assigning a claim to unnamed experts or unnamed "many parties."

**Before:**
> ด้วยลักษณะเฉพาะตัว แม่น้ำสายนี้จึงเป็นที่สนใจของนักวิจัยและนักอนุรักษ์ ผู้เชี่ยวชาญเชื่อว่ามันมีบทบาทสำคัญอย่างยิ่งต่อระบบนิเวศของภูมิภาค
**After:**
> นักวิจัยและนักอนุรักษ์ศึกษาแม่น้ำสายนี้เพราะลักษณะทางน้ำที่ไม่เหมือนสายอื่นในพื้นที่

Name a real source when the source text has one. Otherwise cut the claim. Never invent a source.

### 6. Formulaic "challenges and future" sections

**Words to watch:** แม้จะเผชิญกับความท้าทาย, อย่างไรก็ตาม ด้วยศักยภาพที่มีอยู่, ยังคงเติบโตอย่างต่อเนื่อง, ก้าวต่อไปอย่างมั่นคง, ความท้าทายและโอกาส, แนวโน้มในอนาคต

**Problem:** A stock closing section about challenges or the future that repeats vague claims instead of adding facts.

**Before:**
> แม้จะเจริญรุ่งเรืองทางอุตสาหกรรม แต่เขตนี้ก็ยังเผชิญกับความท้าทายที่พบได้ทั่วไปในเขตเมือง ทั้งปัญหาการจราจรและการขาดแคลนน้ำ อย่างไรก็ตาม ด้วยทำเลที่ตั้งเชิงยุทธศาสตร์และโครงการต่าง ๆ ที่กำลังดำเนินอยู่ เขตนี้ยังคงเติบโตอย่างต่อเนื่อง
**After:**
> เขตนี้มีปัญหารถติดและน้ำไม่พอใช้เป็นประจำ

---

## Group 2: Sentence structure

### 7. Overused AI words

**High-frequency words:** อย่างไรก็ตาม, อีกทั้ง, ยิ่งไปกว่านั้น, นอกจากนี้, ทั้งนี้, ดังนั้น, สะท้อน, ตอกย้ำ, ยกระดับ, ขับเคลื่อน, ผลักดัน, บูรณาการ, องค์รวม, ไร้รอยต่อ, ครบวงจร, อย่างมีประสิทธิภาพ, อย่างยั่งยืน, ในยุคดิจิทัล, ภูมิทัศน์ (abstract sense), ถักทอ, เปี่ยมด้วย, ทรงพลัง, สำคัญอย่างยิ่งยวด, เชิงลึก, ต่อยอด, พลิกโฉม, โดดเด่น, น่าจับตามอง, องค์ความรู้

**Problem:** None of these are wrong on their own, but AI uses them far more often than people do, especially clustered in one paragraph.

**Before:**
> นอกจากนี้ อาหารไทยยังโดดเด่นด้วยการใช้สมุนไพรพื้นถิ่น อีกทั้งยังสะท้อนถึงภูมิปัญญาที่ถักทอกันมาอย่างยาวนาน ซึ่งตอกย้ำถึงความอุดมสมบูรณ์ของภูมิทัศน์ทางอาหารไทยได้อย่างแท้จริง
**After:**
> อาหารไทยใช้สมุนไพรสดเป็นหลัก ทั้งตะไคร้ ข่า และใบมะกรูด ซึ่งหาได้ในครัวเรือนทั่วไป

### 8. Turning verbs into nouns (การ / ความ / ดำเนินการ)

**Words to watch:** ดำเนินการ, ทำการ, มีการ, เกิดการ, ให้เกิดความ, มีความสามารถในการ, มีความจำเป็นต้อง, การดำเนินการ, ความเป็น

**Problem:** Wrapping a plain verb in การ or ความ and prefixing an empty verb like ดำเนินการ. The sentence gets longer, the meaning stays the same. **This is the strongest single tell in AI-written Thai.**

**Before:**
> ทีมงานได้ดำเนินการปรับปรุงประสิทธิภาพของระบบ เพื่อให้เกิดการใช้งานที่รวดเร็วยิ่งขึ้น และมีการตรวจสอบความถูกต้องของข้อมูลก่อนทำการบันทึก
**After:**
> ทีมปรับให้ระบบทำงานเร็วขึ้น และตรวจข้อมูลก่อนบันทึก

### 9. Redundant word pairs

**Words to watch:** ปรับปรุงและพัฒนา, ส่งเสริมและสนับสนุน, ตรวจสอบและติดตาม, รวดเร็วและทันท่วงที, มั่นคงและปลอดภัย, ครบครันและสมบูรณ์แบบ, ถูกต้องและแม่นยำ, ชัดเจนและโปร่งใส

**Problem:** Near-synonym pairs used to fill the mouth, adding no meaning. Pick one word. If the two really do mean different things, split them into two separate statements.

**Before:**
> ระบบใหม่ช่วยส่งเสริมและสนับสนุนให้การทำงานเป็นไปอย่างรวดเร็วและทันท่วงที พร้อมทั้งตรวจสอบและติดตามข้อมูลได้อย่างถูกต้องและแม่นยำ
**After:**
> ระบบใหม่ทำให้งานเสร็จเร็วขึ้น และตามดูข้อมูลย้อนหลังได้

### 10. ถูก used as an English-style passive

**Problem:** In Thai, ถูก carries an adverse sense — something bad happening to the subject (ถูกไล่ออก, ถูกขโมย, ถูกตัดสิทธิ์). Translating every English passive into ถูก gives the sentence the wrong tone. The best fix is to **name who does the action**. If you genuinely must avoid the agent in formal text, use ได้รับการ or drop the subject entirely.

**Before:**
> ข้อมูลจะถูกบันทึกลงในฐานข้อมูล จากนั้นอีเมลจะถูกส่งไปยังผู้ใช้โดยอัตโนมัติ และรายงานจะถูกสร้างขึ้นในตอนสิ้นวัน
**After:**
> ระบบจะบันทึกข้อมูลลงฐานข้อมูล แล้วส่งอีเมลหาผู้ใช้อัตโนมัติ ตอนสิ้นวันจะสร้างรายงานให้

Keep ถูก when it conveys real harm, as in บัญชีถูกระงับ or ไฟล์ถูกลบ.

### 11. Sentence patterns translated straight from English

| Calque | Rewrite |
| --- | --- |
| มันเป็นสิ่งสำคัญที่จะต้องทราบว่า X | X (drop the opener) |
| ไม่เพียงแต่ X เท่านั้น แต่ยัง Y อีกด้วย | ทั้ง X และ Y / X และยัง Y |
| ในโลกของ X ที่เปลี่ยนแปลงอย่างรวดเร็ว | (cut it, start with the point) |
| เมื่อพูดถึง X แล้ว | (cut it) |
| หนึ่งใน X ที่ดีที่สุด | X ที่ดีที่สุดตัวหนึ่ง |
| ในตอนท้ายของวัน | สุดท้ายแล้ว |
| ทำให้มั่นใจได้ว่า | ทำให้ / จะได้ |
| X มีบทบาทในการ Y | X ทำหน้าที่ Y / X ใช้ Y |
| ด้วยเหตุนี้จึงกล่าวได้ว่า | (cut it) |

**Before:**
> ในโลกของการพัฒนาซอฟต์แวร์ที่เปลี่ยนแปลงอย่างรวดเร็ว มันเป็นสิ่งสำคัญที่จะต้องทราบว่าการเขียน test ไม่เพียงแต่ช่วยลดข้อผิดพลาดเท่านั้น แต่ยังทำให้มั่นใจได้ว่าโค้ดจะทำงานได้ตามที่คาดหวังอีกด้วย
**After:**
> การเขียน test ช่วยให้เจอ bug เร็วขึ้น และรู้ทันทีเวลาแก้โค้ดแล้วของเดิมพัง

### 12. Chaining ซึ่ง until the sentence never ends

**Problem:** AI strings clauses together with ซึ่ง, โดย, and ทำให้ in imitation of English relative clauses. Thai does not chain that way. Break into shorter sentences, or use ที่ when it genuinely modifies a noun.

**Before:**
> ระบบจะตรวจสอบสิทธิ์ของผู้ใช้ ซึ่งจะเชื่อมต่อกับฐานข้อมูลกลาง ซึ่งเก็บข้อมูลบัญชีทั้งหมดเอาไว้ ซึ่งทำให้สามารถยืนยันตัวตนได้อย่างถูกต้อง
**After:**
> ระบบตรวจสิทธิ์ผู้ใช้กับฐานข้อมูลกลางที่เก็บข้อมูลบัญชีทั้งหมด

### 13. มัน and คุณ inserted for "it" and "you"

**Problem:** Thai drops subjects freely and usually does. Translating `it` and `you` literally scatters มัน and คุณ across the page.

**Before:**
> มันเป็นเรื่องปกติที่คุณจะพบปัญหานี้ เมื่อคุณติดตั้งโปรแกรมครั้งแรก มันจะขอสิทธิ์ผู้ดูแลระบบจากคุณ และคุณจำเป็นต้องอนุญาตเพื่อให้มันทำงานได้
**After:**
> ปัญหานี้เจอบ่อยตอนติดตั้งครั้งแรก โปรแกรมจะขอสิทธิ์ผู้ดูแลระบบ ต้องกดอนุญาตก่อนถึงจะใช้งานได้

### 14. Connectors piled at the head of every paragraph

**Problem:** Every paragraph opens with นอกจากนี้ / อีกทั้ง / ยิ่งไปกว่านั้น / อย่างไรก็ตาม / ทั้งนี้. Any one of these is fine; stacked, they are a tell.

Fix by cutting most of the connectors and letting the order of the content do the connecting. Thai relies on sequence more than on connective words.

**Before:**
> ระบบรองรับการเข้าสู่ระบบด้วยอีเมล นอกจากนี้ ยังรองรับ Google และ LINE อีกทั้งยังจดจำอุปกรณ์ที่เคยเข้าใช้งาน ยิ่งไปกว่านั้น ผู้ใช้ยังสามารถตั้งค่า 2FA ได้ อย่างไรก็ตาม ฟีเจอร์นี้ยังไม่เปิดให้บัญชีองค์กร
**After:**
> ระบบเข้าสู่ระบบได้ด้วยอีเมล Google และ LINE จำอุปกรณ์ที่เคยใช้ได้ และตั้ง 2FA ได้ ยกเว้นบัญชีองค์กรที่ยังไม่เปิดให้ใช้ 2FA

### 15. Forced groups of three

**Problem:** Packing ideas into sets of three so the sentence feels complete, when the real count is two or four.

**Before:**
> งานนี้ประกอบด้วยการบรรยาย เวิร์กช็อป และกิจกรรมสร้างเครือข่าย ผู้เข้าร่วมจะได้รับทั้งความรู้ แรงบันดาลใจ และมุมมองใหม่
**After:**
> งานนี้มีบรรยายกับเวิร์กช็อป และเว้นช่วงให้คุยกันเองระหว่างพัก

### 16. False ตั้งแต่ X ไปจนถึง Y ranges

**Problem:** Using ตั้งแต่...ไปจนถึง when X and Y are not on the same axis, so there is no actual range.

**Before:**
> หนังสือเล่มนี้พาเราเดินทางตั้งแต่จุดกำเนิดของเอกภพไปจนถึงโครงข่ายจักรวาลอันยิ่งใหญ่ ตั้งแต่การเกิดและดับของดวงดาวไปจนถึงปริศนาของสสารมืด
**After:**
> หนังสือเล่มนี้พูดถึงบิกแบง การก่อตัวของดาวฤกษ์ และทฤษฎีเรื่องสสารมืดในปัจจุบัน

---

## Group 3: Spacing, punctuation, and formatting

### 17. English-style spacing between words

**Problem:** Thai runs together inside a phrase and spaces only at phrase or clause boundaries. Text that came through a translation tool or a word segmenter often spaces every word.

**Before:**
> ระบบ จะ ทำการ ตรวจสอบ ข้อมูล ก่อน บันทึก ลง ฐานข้อมูล
**After:**
> ระบบจะตรวจข้อมูลก่อนบันทึกลงฐานข้อมูล

The opposite is also a problem: one unbroken run with nowhere to breathe. Space at the joints between ideas.

### 18. Sentence-final periods and comma-separated lists

**Problem:** Thai does not put a full stop at the end of a sentence, and rarely uses commas to separate list items — it uses spaces. Translated text usually carries both over.

**Before:**
> ระบบจะบันทึกข้อมูล, ส่งอีเมล, และปิดงาน.
**After:**
> ระบบจะบันทึกข้อมูล ส่งอีเมล แล้วปิดงาน

Exceptions: commas are fine for lists of long or ambiguous proper nouns, as in "BBC, The New York Times และ Financial Times", and periods stay in abbreviations like พ.ศ. and น.ส.

### 19. Em and en dashes

**Rule:** Thai writing does not normally use em dashes (—) or en dashes (–). The final rewrite should have none, unless the writer's own sample uses them. Replace with a space, parentheses, a colon, or a sentence break. Also check for spaced dashes (` — `) and double hyphens (` -- `) used as dashes.

**Before:**
> คำนี้ถูกผลักดันโดยหน่วยงานรัฐ—ไม่ใช่โดยคนในพื้นที่เอง—แต่ก็ยังถูกใช้ต่อมาเรื่อย ๆ
**After:**
> คำนี้หน่วยงานรัฐเป็นคนผลักดัน ไม่ใช่คนในพื้นที่ แต่ก็ยังใช้กันต่อมาเรื่อย ๆ

Before returning the rewrite, search for `—` and `–` and remove every one.

### 20. Too much bold text

**Problem:** Bolding words and phrases with no clear reason.

**Before:**
> ระบบนี้ผสาน **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)** และเครื่องมือเชิงกลยุทธ์อย่าง **Business Model Canvas (BMC)** เข้าด้วยกัน
**After:**
> ระบบนี้ใช้ OKR, KPI และ Business Model Canvas ร่วมกัน

### 21. Lists where every item starts with a bold mini-heading

**Problem:** A vertical list in which every item opens with a bold label and a colon, when the content would run fine as one paragraph.

**Before:**
> - **ประสบการณ์ผู้ใช้:** ปรับปรุงหน้าตาให้ใช้งานง่ายขึ้นอย่างมีนัยสำคัญ
> - **ประสิทธิภาพ:** เพิ่มความเร็วผ่านการปรับปรุงอัลกอริทึม
> - **ความปลอดภัย:** เสริมความแข็งแกร่งด้วยการเข้ารหัสแบบ end-to-end
**After:**
> เวอร์ชันนี้ปรับหน้าตาใหม่ให้โหลดเร็วขึ้น และเพิ่มการเข้ารหัสแบบ end-to-end

### 22. Decorative emojis

**Before:**
> 🚀 **เปิดตัว:** สินค้าจะวางขายไตรมาส 3
> 💡 **ข้อค้นพบสำคัญ:** ผู้ใช้ชอบความเรียบง่าย
> ✅ **ขั้นตอนถัดไป:** นัดประชุมติดตามผล
**After:**
> สินค้าจะวางขายไตรมาส 3 ผลวิจัยพบว่าผู้ใช้ชอบแบบที่เรียบง่ายกว่า ขั้นถัดไปคือนัดประชุมติดตามผล

### 23. Curly quotes, mixed numerals, and mixed era systems

**Problem:** ChatGPT often emits curly quotes (“...”) where the document uses straight quotes ("..."). It also mixes Thai numerals (๑๒๓) with Arabic ones (123) in the same document, or switches between พ.ศ. and ค.ศ. partway through.

Pick one of each and follow whatever the source document already uses. If the source uses พ.ศ., do not convert the years to ค.ศ. — that is changing a fact, not a style.

### 24. Headings translated into long noun phrases

**Problem:** Thai headings translated from English tend to become long noun phrases that all start with การ. Good Thai headings are shorter.

**Before:**
> ## การดำเนินการเจรจาเชิงกลยุทธ์และการสร้างความร่วมมือระดับโลก
**After:**
> ## การเจรจาและความร่วมมือระหว่างประเทศ

---

## Group 4: Chatbot artifacts

### 25. Chatbot text left in the content

**Words to watch:** แน่นอนครับ!, ได้เลยครับ, ยินดีครับ, นี่คือ...ที่คุณต้องการ, หวังว่าจะเป็นประโยชน์นะครับ, หากต้องการให้ขยายความส่วนไหน บอกได้เลย, ต้องการให้ผมช่วยอะไรอีกไหม, สรุปให้แบบเข้าใจง่ายนะครับ, ลองดูนะครับ

**Before:**
> ได้เลยครับ นี่คือภาพรวมของการปฏิวัติฝรั่งเศสครับ หวังว่าจะเป็นประโยชน์นะครับ หากต้องการให้ขยายความส่วนไหนเพิ่ม บอกได้เลยครับ
**After:**
> การปฏิวัติฝรั่งเศสเริ่มขึ้นในปี 1789 จากวิกฤตการคลังและการขาดแคลนอาหารที่นำไปสู่ความไม่สงบเป็นวงกว้าง

### 26. Overly agreeable opening

**Words to watch:** เป็นคำถามที่ดีมากครับ!, คุณเข้าใจถูกต้องแล้ว, ประเด็นที่คุณยกมานั้นยอดเยี่ยมมาก, ถูกต้องเลยครับ, คุณคิดได้ดีมาก

**Before:**
> เป็นคำถามที่ดีมากครับ! คุณเข้าใจถูกต้องแล้วว่าเรื่องนี้ค่อนข้างซับซ้อน และประเด็นเรื่องปัจจัยทางเศรษฐกิจที่คุณยกมาก็ยอดเยี่ยมมาก
**After:**
> ปัจจัยทางเศรษฐกิจที่ว่ามาเกี่ยวข้องกับเรื่องนี้โดยตรง

### 27. Admitting a gap, then guessing to fill it

**Words to watch:** จากข้อมูลล่าสุดที่มี, ณ ขณะที่เขียน, เท่าที่มีข้อมูลเปิดเผย, ไม่มีข้อมูลปรากฏต่อสาธารณะ, คาดว่า, น่าจะ, เชื่อกันว่า, สันนิษฐานว่า, เก็บตัวเงียบ, ไม่เปิดเผยเรื่องส่วนตัว

**Problem:** The model says it could not find a source, then fills the gap with something plausible. State plainly that the source does not have it, or cut the sentence. Never present a guess as fact.

**Before:**
> ไม่ปรากฏข้อมูลชีวิตช่วงต้นของเธอต่อสาธารณะ ซึ่งน่าจะเป็นเพราะเธอเก็บตัวเงียบและไม่เปิดเผยเรื่องส่วนตัว เธอน่าจะเติบโตมาในครอบครัวชนชั้นกลาง อันเป็นที่มาของความสนใจด้านการศึกษาในเวลาต่อมา
**After:**
> ไม่มีข้อมูลชีวิตช่วงต้นของเธอในแหล่งที่อ้างอิงได้ (or drop the section entirely)

### 28. Inconsistent sentence-final particles

**Problem:** Switching between ครับ and ค่ะ in one document, adding particles to technical documentation that should have none, or dusting นะคะ / นะครับ onto every sentence until the reader feels handled.

**Before:**
> ขั้นแรกให้เปิด terminal ขึ้นมาก่อนนะคะ จากนั้นพิมพ์คำสั่งตามด้านล่างนี้เลยครับ แล้วรอจนกว่าจะติดตั้งเสร็จนะคะ
**After:**
> เปิด terminal แล้วรันคำสั่งด้านล่าง รอจนติดตั้งเสร็จ

---

## Group 5: Filler and hedging

### 29. Filler phrases

| Before | After |
| --- | --- |
| เพื่อที่จะให้บรรลุเป้าหมายดังกล่าว | เพื่อ... |
| เนื่องจากข้อเท็จจริงที่ว่าฝนตก | เพราะฝนตก |
| ณ ช่วงเวลานี้ | ตอนนี้ |
| ในกรณีที่คุณต้องการความช่วยเหลือ | ถ้าต้องการความช่วยเหลือ |
| ระบบมีความสามารถในการประมวลผล | ระบบประมวลผลได้ |
| เป็นที่น่าสังเกตว่าข้อมูลแสดงให้เห็นว่า | ข้อมูลแสดงว่า |
| มีความจำเป็นต้องทำการตรวจสอบ | ต้องตรวจสอบ |
| ในส่วนของเรื่องนี้ | เรื่องนี้ |

### 30. Stacked hedges

**Words to watch:** อาจกล่าวได้ว่า, ค่อนข้างที่จะ, มีแนวโน้มที่อาจจะ, ในบางกรณีอาจ, ก็เป็นไปได้ว่า, ประมาณหนึ่ง, พอสมควร

**Problem:** Repeated editing piles one qualifier on another until every claim sounds uncertain. Keep a hedge only when the source supports it and the meaning needs it.

**Before:**
> อาจกล่าวได้ว่านโยบายนี้ค่อนข้างที่จะมีแนวโน้มส่งผลกระทบต่อผลลัพธ์ในบางกรณีอยู่พอสมควร
**After:**
> นโยบายนี้อาจส่งผลต่อผลลัพธ์

### 31. Generic optimistic endings

**Problem:** Closing on vague optimism instead of the last useful fact.

**Before:**
> อนาคตของบริษัทยังคงสดใส พร้อมก้าวต่อไปอย่างมั่นคงและยั่งยืน นับเป็นอีกหนึ่งก้าวสำคัญในทิศทางที่ถูกต้อง
**After:**
> (Cut the paragraph. End on the previous fact. If the source states real plans, use those.)

### 32. Pretending to reveal a deeper truth

**Words to watch:** คำถามที่แท้จริงคือ, โดยแก่นแท้แล้ว, ในความเป็นจริงแล้ว, สิ่งที่สำคัญจริง ๆ คือ, หัวใจสำคัญอยู่ที่, ลึกลงไปกว่านั้น, ประเด็นที่ลึกกว่านั้นคือ

**Before:**
> คำถามที่แท้จริงคือทีมจะปรับตัวได้หรือไม่ โดยแก่นแท้แล้ว สิ่งที่สำคัญจริง ๆ คือความพร้อมขององค์กร
**After:**
> คำถามคือทีมจะปรับตัวได้ไหม ซึ่งขึ้นอยู่กับว่าองค์กรยอมเปลี่ยนวิธีทำงานเดิมหรือเปล่า

### 33. Announcing the next point instead of making it

**Words to watch:** มาดูกันว่า, เรามาเจาะลึกกันเลย, ก่อนอื่นเลย, นี่คือสิ่งที่คุณต้องรู้, ไปกันเลย, เดี๋ยวจะอธิบายให้ฟัง, ขอเกริ่นก่อนว่า, บอกไว้ก่อนนิดนึง

**Before:**
> เรามาเจาะลึกกันว่า caching ใน Next.js ทำงานยังไง นี่คือสิ่งที่คุณต้องรู้
**After:**
> Next.js ทำ cache หลายชั้น ทั้ง request memoization, data cache และ router cache

The casual register has the same problem. Remove the announcement, not just its formality.

**Before:**
> เรื่องนี้ผมเจอมากับตัวเลย ฟังให้ดีนะ webpack dev server ไม่ได้ส่ง CORS header มาให้ตั้งแต่แรก
**After:**
> webpack dev server ไม่ได้ส่ง CORS header มาให้ตั้งแต่แรก

### 34. First sentence repeats the heading

**Problem:** A one-line paragraph under a heading that only restates the heading before the real content starts. Cut it.

**Before:**
> ## ประสิทธิภาพ
>
> ความเร็วเป็นเรื่องสำคัญ
>
> ถ้าหน้าเว็บโหลดช้า ผู้ใช้จะปิดทิ้ง
**After:**
> ## ประสิทธิภาพ
>
> ถ้าหน้าเว็บโหลดช้า ผู้ใช้จะปิดทิ้ง

### 35. Formulaic sayings and borrowed English idioms

**Words to watch:** X คือ Y ของ Z, ข้อมูลคือน้ำมันชนิดใหม่, เปรียบเสมือน, ไม่ต่างอะไรกับ, เกมเปลี่ยน, ดาบสองคม, ภาษาของ..., สกุลเงินของ..., สถาปัตยกรรมของ...

**Problem:** Turning an ordinary claim into a saying that sounds deep but adds no detail. Replace the saying with the specific claim.

**Before:**
> ความสมมาตรคือภาษาของความไว้วางใจ ส่วนประสิทธิภาพนั้นเปรียบเสมือนดาบสองคมเมื่อทีมลืมมิติของมนุษย์
**After:**
> เลย์เอาต์ที่สมมาตรทำให้ผู้ใช้เดาตำแหน่งของแต่ละส่วนได้ง่ายกว่า และทีมมักปรับ workflow จนลืมดูว่าคนใช้งานจริงทำอะไรบ้าง

### 36. Fake-candid openings

**Words to watch:** บอกตรง ๆ นะ, เอาจริง ๆ, พูดกันตามตรง, เรื่องของเรื่องคือ, จะบอกให้ก็ได้ — when used as a standalone hook before an ordinary point.

**Before:**
> คุ้มกับราคาไหม? เอาจริง ๆ นะ มันขึ้นอยู่กับว่าคุณจะได้ใช้บ่อยแค่ไหน
**After:**
> จะคุ้มราคาหรือไม่ ขึ้นอยู่กับว่าได้ใช้บ่อยแค่ไหน

### 37. Answering objections no one raised

**Words to watch:** ไม่ได้จะบอกว่า, ต้องบอกก่อนว่า, อย่าเข้าใจผิด, ไม่ได้หมายความว่า, หลายคนอาจคิดว่า...แต่, จะมองอีกมุมก็ได้ แต่

**Problem:** Answering an objection that never appears in the text. Watch for a sentence about what the writer does *not* mean, when that topic appears nowhere else.

**Before:**
> เรื่องนี้ไม่ได้เกี่ยวกับความยาวของ prompt เป็นหลัก และผมก็ไม่ได้จะบอกว่าเอกสารไม่สำคัญ จะจัดหมวดปัญหาแบบอื่นก็ได้ แต่ประเด็นอยู่ที่ว่า agent เอาคำสั่งไปใช้ตอนลงมือทำได้จริงหรือเปล่า
**After:**
> ประเด็นอยู่ที่ว่า agent เอาคำสั่งไปใช้ตอนลงมือทำได้จริงหรือเปล่า

Remove only the unsupported defense. If it contains a real claim, state that claim directly. Keep an objection when the text names its source or answers it in full.

### 38. Rejecting fake alternatives

**Words to watch:** ทางเลือกหนึ่งที่ดูน่าสนใจคือ, หลายคนอาจเลือกที่จะ, วิธีที่ดูเหมือนจะง่ายที่สุดคือ, อาจจะคิดว่า...แต่, บางคนอาจแนะนำให้

**Problem:** Introducing an option no reader would consider, rejecting it in one clause, and never mentioning it again. Usually a leftover from drafting. Cut the fake option and state the real constraint.

**Before:**
> session token จะหมุนทุก 24 ชั่วโมง ทางเลือกหนึ่งที่ดูน่าสนใจคือหมุนด้วยการ restart auth service ผ่าน cron job แต่วิธีนั้นจะทำให้ session ที่ใช้งานอยู่หลุดทั้งหมด ระบบจึงหมุน token แบบ in place และ client จะ refresh ให้เองโดยผู้ใช้ไม่รู้สึก
**After:**
> session token จะหมุนทุก 24 ชั่วโมงแบบ in place และ client จะ refresh ให้เองโดยผู้ใช้ไม่รู้สึก

One rejected option may be valid. Several short, unrelated rejections are a stronger signal. Ask what each sentence adds. If it only records an earlier edit, rewrite the paragraph around its main point.

---

## Check for false positives

### What not to flag

Plenty of Thai writers genuinely write this way. Do not treat any item below as proof on its own.

- **Bureaucratic Thai in official documents.** หนังสือราชการ, announcements, contracts, and legal text have their own conventions. ทั้งนี้, ดังกล่าว, and จึงเรียนมาเพื่อโปรดทราบ are correct there. Do not convert them to spoken Thai.
- **ครับ / ค่ะ.** Normal polite Thai. The tell is inconsistency and wrong context, not the particle itself.
- **A single connector.** One นอกจากนี้ is fine. It only becomes a tell when they stack.
- **Long sentences.** Thai naturally runs longer than English. Do not chop it to English sentence length. The problem is ซึ่ง-chaining, not length.
- **Repeating a name.** Thai repeats the noun instead of using a pronoun, and that is natural. Do not "fix" it by cycling synonyms — that makes it read *more* like AI.
- **Correct uses of ถูก.** When it conveys real harm, as in ถูกระงับ or ถูกปฏิเสธ, it is right.
- **Established loanwords.** คอมพิวเตอร์, อินเทอร์เน็ต, ไฟล์, เมนู are ordinary Thai, not translation residue.
- **Spacing before ๆ.** Both ต่าง ๆ and ต่างๆ are in real use. Follow whatever the document does. Not a signal.
- **Mixing English into Thai.** Thai speakers in tech genuinely talk this way. Not a tell.
- **Clean spelling and consistent formatting.** Edited work is clean too. Polish does not equal AI.
- **Quoted text, titles, and proper names.** Do not rewrite a watched phrase inside a quotation or an example where the phrase is being discussed rather than used.
- **Text written before 30 November 2022.** ChatGPT's public launch. Older text is, with rare exceptions, not AI-written.

When unsure, look for several patterns together. One dash proves nothing. Brochure language, stacked connectors, and ดำเนินการ in the same paragraph is much stronger evidence.

### Human details to keep

These carry the writer's voice. Keep them unless they hurt the meaning.

- **Specific, unusual details.** A shop name, a soi number, a real quote, or a phrase like "พี่ที่เคยทำงานอยู่ตึกตรงข้ามหมอฟันผม".
- **Unresolved feelings.** Lines like "ก็ดีอยู่นะ แต่ยังรู้สึกติด ๆ อยู่ บอกไม่ถูกเหมือนกัน".
- **Era-bound slang and references.** Jokes, memes, or trending words tied to a specific year. Models lag on these.
- **Dialect.** Isan, Northern, or Southern words the writer already uses.
- **Mood particles.** เหอะ, อ่ะ, แหละ, ดิ, ป่ะ, เฉย in casual contexts.
- **Uneven sentence length.** Real writing alternates short and long. AI Thai tends to hold one mid-length cadence.
- **Parenthetical asides and self-corrections.** "(จริง ๆ อยากเขียนว่าเกือบ แต่มันแน่นอนไปแล้ว)". Models rarely interrupt themselves.
- **Deliberate choices.** If the writer can explain why they picked that word, keep it.

---

## How to return the result

**Pasted text (default).** Return three parts: the draft, a short list of remaining AI patterns, and the final rewrite.

**File mode.** When the user names a file, run the full rewrite process but write only the final text to the file. Change prose only. Leave code blocks, YAML, data, and link targets untouched. Then give the user a short summary of what changed.

**Embedded mode.** When another skill calls this one as a style pass for a commit message, pull request, wiki page, checklist, or other Thai document, return only the final text with no commentary.

## Rewrite process

1. Read the source and mark each pattern you find.
2. Write a draft, then **read it aloud.** Thai judges better by ear than by eye. If reading aloud snags, the rhythm is still wrong.
3. Run the Thai-specific sweeps:
   - Search ดำเนินการ, ทำการ, มีการ, ความสามารถในการ and turn them back into verbs (§8).
   - Search ถูก and ask whether real harm is involved. If not, name the actor (§10).
   - Search ซึ่ง used more than once in a single sentence (§12).
   - Search มัน and คุณ that can be dropped (§13).
   - Read the first words of every paragraph in sequence. If several repeat the same connector, cut them (§14).
   - Search `—`, `–`, and sentence-final periods on Thai sentences (§18, §19).
   - Confirm particles and pronouns are consistent across the whole piece (§28).
4. Ask two questions:
   - **"What still reads as AI-written?"**
   - **"Did the rewrite add or lose any name, number, date, quote, citation, or other claim?"**
   Treat both an unsupported addition and a lost claim as an error.
5. Write the final version. State each point naturally across the whole paragraph rather than patching one flagged phrase at a time. If a sentence stays awkward, rewrite the paragraph around its main point.

Return the result in the form required by [How to return the result](#how-to-return-the-result).

## Source

Adapted from the [humanizer](https://github.com/blader/humanizer) skill (MIT), which draws on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

Patterns carried over from the original: inflated importance, name-dropping, vague sources, chatbot artifacts, filler, and fake alternatives. Patterns added specifically for Thai: §8 nominalization, §9 redundant pairs, §10 ถูก-passive, §11 English calques, §12 ซึ่ง-chaining, §13 มัน/คุณ, §17 spacing, §18 periods and commas, §23 numerals and era systems, §24 noun-phrase headings, and §28 particles, plus the register and technical-term sections above.

Wikipedia's core point is that an LLM predicts the next token statistically, so output drifts toward the most likely result that fits the widest range of cases. In Thai, that mechanism produces sentences with English structure inside them, wrapped in formal Thai vocabulary.
