#!/usr/bin/env python3
"""
Batch Plan Generator - Creates plan.json for all 81 pending ideas.
All prompts written by Claude (no AI generation).
Author: BoBo Art | Page size: 8.5x8.5 (square) | Pages: 50 per book
"""

import json
import os
import shutil
import re

BASE_DIR = "/Users/hoangtran/Documents/Github/aws kdp"
IDEAS_DIR = os.path.join(BASE_DIR, "ideas")
DONE_DIR = os.path.join(IDEAS_DIR, "done")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

AUTHOR = {"first_name": "BoBo", "last_name": "Art"}
PAGE_SIZE = "8.5x8.5"
SIZE_TAG = "SQUARE format (1:1 aspect ratio)"
PAGE_COUNT = 50

# Adult prompt prefix
ADULT_PREFIX = (
    "Black and white line art illustration for an adult coloring book, "
    "cute cozy medium-detail aesthetic, bold clean outlines, large open shapes for easy coloring, "
    "no shading. IMPORTANT: The illustration must NOT have any border, frame, or rectangular outline around the edges. "
    "The line art should extend naturally to the edges with NO enclosing box or boundary line. "
    "White background. SQUARE format (1:1 aspect ratio). "
)

ADULT_SUFFIX = (
    "Clean bold outlines, cozy relaxing environment, easy-to-color shapes, "
    "adult coloring book page. The artwork must have NO outer border, NO enclosing rectangle, NO frame around the image."
)

# Kids prompt prefix
KIDS_PREFIX = (
    "A children's coloring book page in SQUARE format (1:1 aspect ratio). "
    "Black and white line art only. "
)

KIDS_SUFFIX = (
    "Thick, clean, bold outlines. Simple enough for kids ages 6-12 to color. "
    "White background. The drawing fills most of the page. "
    "No shading, no gray tones. IMPORTANT: NO outer border, NO enclosing rectangle, NO frame around the image. "
    "Style: cute, friendly, appealing to children."
)


def adult_prompt(scene, fg, mg, bg):
    """Generate a full adult coloring page prompt."""
    return (
        f'{ADULT_PREFIX}'
        f'Scene: {scene} '
        f'Foreground: {fg} '
        f'Midground: {mg} '
        f'Background: {bg} '
        f'{ADULT_SUFFIX}'
    )


def kids_prompt(subject):
    """Generate a full kids coloring page prompt."""
    return f'{KIDS_PREFIX}{subject} {KIDS_SUFFIX}'


# =============================================================================
# ALL 81 BOOKS - Metadata + 50 prompts each
# =============================================================================

BOOKS = {}

# ─────────────────────────────────────────────────────────────────────────────
# 19. LAVENDER DREAMS (adults, realistic)
# ─────────────────────────────────────────────────────────────────────────────
BOOKS["lavender_dreams"] = {
    "filename": "19_lavender_dreams.md",
    "theme_key": "lavender_dreams",
    "concept": "Lavender Dreams",
    "audience": "adults",
    "title": "Lavender Dreams: Coloring Book for Adults, Bold and Easy",
    "subtitle": "50 Relaxing Provence-Inspired Lavender Fields, Cottages, and Garden Scenes for Stress Relief",
    "description": (
        "<h4>Lose yourself in the gentle beauty of endless lavender fields...</h4><br>"
        "Step into the dreamy world of Provence with 50 beautifully designed coloring pages. "
        "Each scene captures the romantic charm of lavender meadows, stone cottages, vintage vases, "
        "and peaceful garden pathways. Bold, easy-to-color outlines make every page a relaxing escape.<br><br>"
        "<b>What's Inside:</b><br>"
        "&#x2022; 50 unique lavender-themed illustrations<br>"
        "&#x2022; Provence cottages, lavender rows, vintage still life, garden paths<br>"
        "&#x2022; Single-sided pages to prevent bleed-through<br>"
        "&#x2022; Large 8.5 x 8.5 inch square pages<br>"
        "&#x2022; Bold outlines perfect for colored pencils, markers, and gel pens<br><br>"
        "<b>Perfect For:</b><br>"
        "&#x2022; Stress relief and mindful relaxation<br>"
        "&#x2022; Gift for flower lovers and Francophiles<br>"
        "&#x2022; Cozy evenings and creative self-care<br>"
        "&#x2022; All skill levels from beginners to experienced colorists<br><br>"
        "<b>Pick up your pencils and let the calming scent of lavender fill your imagination.</b>"
    ),
    "keywords": [
        "lavender field coloring pages relaxation calm",
        "french countryside provence illustration botanical",
        "flower garden cottagecore adult coloring women",
        "stress relief mindfulness art therapy creative",
        "large print simple designs colored pencils markers",
        "gift idea mother birthday christmas nature lover",
        "bold easy floral scenery vintage rustic aesthetic"
    ],
    "categories": [
        "Crafts, Hobbies & Home / Coloring Books for Grown-Ups / Flowers & Landscapes",
        "Crafts, Hobbies & Home / Coloring Books for Grown-Ups / General"
    ],
    "reading_age": "",
    "cover_prompt": (
        "Full-color illustration, warm cozy botanical aesthetic, SQUARE format (1:1 aspect ratio). "
        "A breathtaking Provence lavender field at golden hour with perfectly lined rows of blooming purple lavender stretching to the horizon. "
        "A charming stone cottage with blue shutters sits among the lavender. A vintage bicycle with a basket of lavender leans against a stone wall. "
        "Bees and butterflies dance among the flowers. Soft warm golden sunlight. Dreamy pastel sky with wispy clouds. "
        "Premium cozy cottagecore aesthetic, vibrant warm purple, gold, and green palette. DO NOT include any text in the image."
    ),
    "page_prompts": [
        adult_prompt(
            "Endless rows of lavender stretching to the horizon under a wide sky.",
            "Large lavender stalks with detailed flower clusters, a straw hat resting on the ground, scattered petals.",
            "Neat rows of lavender bushes curving gently, a wooden post with a hanging lantern.",
            "Rolling Provence hills in the distance, a few fluffy clouds, distant cypress trees."
        ),
        adult_prompt(
            "A charming stone cottage surrounded by a lavender garden.",
            "A wooden gate with climbing roses, a watering can, a basket of fresh lavender.",
            "The cottage with blue shutters and a wooden door, window boxes overflowing with flowers, a cat sitting on the doorstep.",
            "A stone chimney with gentle smoke, birds perched on the roofline, a blue sky with soft clouds."
        ),
        adult_prompt(
            "A vintage bicycle leaning against a stone wall with lavender in its basket.",
            "The bicycle with a woven basket filled with lavender bouquets, cobblestone path, fallen petals.",
            "A stone wall with trailing ivy, an old wooden bench, potted lavender plants.",
            "A Provence countryside vista with distant lavender fields, a church steeple, gentle hills."
        ),
        adult_prompt(
            "A lavender harvest scene with a worker gathering bundles.",
            "A large woven basket overflowing with lavender bundles, gardening gloves, pruning shears.",
            "Rows of harvested and unharvested lavender, a wheelbarrow, a sun hat on a post.",
            "A farmhouse in the distance, a stone wall, tall poplar trees lining the horizon."
        ),
        adult_prompt(
            "A cozy window with lavender pots on the windowsill overlooking lavender fields.",
            "Three clay pots of blooming lavender, a teacup with saucer, a small book.",
            "An arched window with wooden shutters, lace curtains gently blowing, a cozy cushion on the seat.",
            "A panoramic view of lavender fields through the window, distant mountains, a soft sunset sky."
        ),
        adult_prompt(
            "A lavender bouquet in a vintage ceramic vase on a rustic table.",
            "A large bouquet of lavender in a decorated vase, scattered sprigs, a ribbon, dried flowers.",
            "A rustic wooden table with a linen runner, a stack of old books, a candle in a holder.",
            "A kitchen shelf with jars of dried herbs, a window showing a garden, hanging dried lavender bundles."
        ),
        adult_prompt(
            "Bees buzzing among lavender flowers in close detail.",
            "Large lavender flower stems with detailed buds, two bees collecting pollen, dewdrops on petals.",
            "A dense lavender bush with multiple stems, a small butterfly resting on a leaf.",
            "A meadow stretching behind with wildflowers, a wooden fence post, a clear sky."
        ),
        adult_prompt(
            "A Provence market stall selling lavender products.",
            "Bundles of dried lavender, lavender soap bars, small bottles of essential oil.",
            "A rustic wooden market stall with a striped canopy, woven baskets, a chalkboard price sign.",
            "Other market stalls in the distance, a cobblestone square, potted olive trees."
        ),
        adult_prompt(
            "A lavender-lined pathway leading to a garden fountain.",
            "Stone steps with lavender bushes on both sides, fallen petals on the path, a garden statue.",
            "A classic stone fountain with gentle water, surrounded by lavender and roses.",
            "A garden wall with an arched gateway, climbing wisteria, birds in the sky."
        ),
        adult_prompt(
            "A cozy reading nook in a lavender garden under a pergola.",
            "An open book on a cushion, a glass of lemonade, a plate of cookies on a side table.",
            "A wooden pergola draped with wisteria and lavender, a comfortable chair with a throw blanket.",
            "A cottage garden with hollyhocks and lavender beds, a birdbath, a gentle breeze shown through fabric."
        ),
        adult_prompt(
            "Sunset over a lavender field with warm golden light.",
            "Close-up lavender stems catching golden light, a straw basket with a blanket, a pair of sandals.",
            "Rolling lavender rows leading to the sun, a lone tree casting a long shadow.",
            "A spectacular sunset sky with streaks of orange and purple, distant farmhouses, gentle hills."
        ),
        adult_prompt(
            "A stone bridge over a stream with lavender growing on the banks.",
            "Wildflowers and lavender along the water's edge, smooth river stones, a dragonfly.",
            "An old stone bridge with an arch, water flowing gently beneath, moss-covered railings.",
            "Weeping willows in the distance, a pastoral meadow, soft clouds."
        ),
        adult_prompt(
            "A cat napping in a lavender field on a warm afternoon.",
            "A curled-up cat among lavender stalks, a butterfly near its nose, scattered petals.",
            "Tall lavender bushes creating a natural bed, a small path winding through.",
            "A Provence farmhouse in the distance, cypress trees, a warm sky."
        ),
        adult_prompt(
            "A lavender distillery with copper equipment and dried herbs.",
            "Copper distillation still with tubes, glass bottles of lavender oil, fresh lavender bundles.",
            "A stone building interior with wooden shelves, drying racks of lavender hanging from ceiling.",
            "A small window showing lavender fields outside, stone walls with old tools hung up."
        ),
        adult_prompt(
            "A picnic scene among lavender fields at midday.",
            "A checkered blanket with a baguette, cheese, wine bottle, and a bowl of cherries.",
            "Lavender rows surrounding the picnic spot, a wide-brimmed sun hat, a flower crown.",
            "A distant village perched on a hillside, a clear blue sky, olive groves."
        ),
        adult_prompt(
            "A lavender wreath hanging on a rustic wooden door.",
            "A beautifully crafted lavender wreath with ribbon, a metal door knocker, a welcome sign.",
            "An old wooden door with iron hinges, stone doorframe with climbing ivy.",
            "A glimpse of a garden through a side window, potted geraniums, a cobblestone step."
        ),
        adult_prompt(
            "A beehive in a lavender garden with bees returning home.",
            "A traditional straw beehive (skep) on a stone platform, bees around the entrance, lavender stems.",
            "A garden with organized lavender rows, a small path, a garden bench nearby.",
            "A cottage roof visible behind trees, a sunset sky, birds flying in formation."
        ),
        adult_prompt(
            "Lavender sachets being crafted on a farmhouse table.",
            "Small fabric sachets filled with lavender, scissors, ribbon, loose lavender buds scattered.",
            "A large farmhouse table with linen cloth, a sewing basket, a teapot with cups.",
            "A kitchen window with gingham curtains, shelves with jars, dried lavender hanging from a rack."
        ),
        adult_prompt(
            "A vintage letterbox surrounded by lavender at a cottage gate.",
            "An ornate metal letterbox with decorative scrollwork, lavender growing around its post.",
            "A wooden garden gate with a lattice top, a stone path leading to a cottage, a climbing rose bush.",
            "A thatched-roof cottage in the distance, a garden with mixed flowers, a gentle sky."
        ),
        adult_prompt(
            "A moonlit lavender field under a starry night sky.",
            "Lavender stems silvered by moonlight, fireflies glowing among the flowers, a lantern on the ground.",
            "Rows of lavender stretching in moonlight, a stone bench at the field's edge.",
            "A full moon in a starry sky, silhouetted cypress trees, distant twinkling village lights."
        ),
        adult_prompt(
            "A girl in a sundress walking through a lavender field, seen from behind.",
            "The hem of a flowing sundress, a hand trailing across lavender tops, a sun hat held loosely.",
            "A narrow path between tall lavender rows, the figure walking into the distance.",
            "A glowing horizon with the sun low in the sky, distant mountains, scattered clouds."
        ),
        adult_prompt(
            "A bird bath surrounded by lavender with a small bird splashing.",
            "A decorative stone bird bath with water ripples, a robin splashing, petals floating.",
            "Lavender bushes encircling the bird bath, a garden path with stepping stones.",
            "A garden shed with tools, a climbing rose trellis, a peaceful blue sky."
        ),
        adult_prompt(
            "A rustic kitchen with lavender drying from the ceiling beams.",
            "A cutting board with bread and honey, a bowl of fresh berries, a knife.",
            "Hanging bundles of drying lavender from wooden ceiling beams, a farmhouse sink with a window.",
            "Shelves with ceramic jars, a vintage clock on the wall, copper pots hanging from hooks."
        ),
        adult_prompt(
            "A stone well in a lavender courtyard with morning mist.",
            "An old stone well with a bucket and rope, moss on the stones, lavender growing at the base.",
            "A courtyard with flagstone floor, lavender in large terracotta pots, a wooden bench.",
            "Morning mist rolling through a garden archway, a stone wall, climbing jasmine."
        ),
        adult_prompt(
            "A lavender field with a row of cypress trees casting shadows.",
            "Close-up lavender in full bloom, a small lizard on a warm stone, scattered seeds.",
            "A dramatic row of tall cypress trees alongside the lavender field, their shadows stretching across.",
            "The Provence landscape with distant blue mountains, a pale sky, a single cloud."
        ),
        adult_prompt(
            "A hand-painted ceramic plate with a lavender design on a table setting.",
            "A decorative plate with painted lavender motifs, silverware, a folded napkin with a lavender sprig.",
            "A beautiful table setting with a white tablecloth, wine glasses, a vase of lavender.",
            "A dining room with French doors open to a garden, sheer curtains, warm afternoon light."
        ),
        adult_prompt(
            "A lavender ice cream cart in a village square.",
            "A vintage ice cream cart with decorative wheels, scoops of lavender ice cream, a waffle cone.",
            "A charming village square with cobblestones, a fountain, outdoor cafe chairs.",
            "Stone buildings with colorful shutters, a church tower, potted flowers on balconies."
        ),
        adult_prompt(
            "A garden journal open on a bench surrounded by lavender.",
            "An open notebook with flower sketches, watercolor paints, pressed lavender flowers.",
            "A wooden garden bench under a tree, a straw bag with gardening books.",
            "A mixed flower garden with lavender borders, a sundial, a butterf ly on a bloom."
        ),
        adult_prompt(
            "A lavender tea set arranged on an outdoor table.",
            "An ornate teapot with lavender decoration, matching cups, a plate of lavender shortbread cookies.",
            "A wrought-iron garden table with a lace cloth, a vase of fresh lavender, a sugar bowl.",
            "A cottage garden with roses and lavender, a trellis arch, songbirds on a branch."
        ),
        adult_prompt(
            "A winding country road through lavender fields with a vintage car.",
            "A classic convertible car parked by the roadside, a picnic basket on the back seat.",
            "A tree-lined country road curving through lavender fields, stone kilometer markers.",
            "Provence hills with vineyards, a distant village, a warm sky with golden light."
        ),
        adult_prompt(
            "A lavender soap-making workshop with ingredients laid out.",
            "Bars of handmade lavender soap with stamped designs, dried flowers, essential oil bottles.",
            "A workshop table with molds, mixing bowls, burlap wrapping, a scale.",
            "Shelves of finished products, a window with herbs on the sill, a brick wall with vintage posters."
        ),
        adult_prompt(
            "A butterfly garden with lavender as the centerpiece planting.",
            "Large swallowtail butterflies on lavender blooms, caterpillars on leaves, flower buds.",
            "A circular garden bed of lavender with stepping stones, a small bench, a birdbath.",
            "A meadow beyond the garden with wildflowers, a wooden fence, distant trees."
        ),
        adult_prompt(
            "A dog resting in the shade of a lavender bush on a warm day.",
            "A sleeping golden retriever under a lavender bush, a water bowl nearby, paw prints in dirt.",
            "A garden path with lavender borders, a garden spigot, a coiled hose.",
            "A stone farmhouse with open windows, laundry drying on a line, a blue sky."
        ),
        adult_prompt(
            "An outdoor painting easel set up in a lavender field.",
            "An easel with a canvas showing a painted lavender scene, a palette with purple paints, brushes.",
            "A folding stool beside the easel, a paint box, a glass jar of water.",
            "The actual lavender field stretching behind, matching the painting, a gentle breeze suggested by grass."
        ),
        adult_prompt(
            "A window box with lavender and herbs on a Provence building.",
            "A long window box overflowing with lavender, rosemary, and thyme, trailing ivy.",
            "A stone building facade with green shutters, an ornate window frame, a flower-carved lintel.",
            "A narrow village street below, a distant church bell tower, a blue sky."
        ),
        adult_prompt(
            "A lavender maze garden with hedged paths from above view.",
            "Detailed hedge edges with lavender plantings, a small fountain at the center.",
            "Curved pathways through organized lavender sections, stone benches at intersections.",
            "A grand estate garden with formal plantings, a distant manor house, topiary trees."
        ),
        adult_prompt(
            "A honey jar with lavender honey and a dipper on a breakfast tray.",
            "A glass jar of golden lavender honey with a wooden dipper, croissants, fresh berries.",
            "A breakfast tray with a white cloth, a small vase of lavender, a cup of coffee.",
            "A bedroom setting with a window showing a lavender garden, lace curtains, morning light."
        ),
        adult_prompt(
            "A clothesline with linens drying in a lavender breeze.",
            "White sheets and linens hanging from a clothesline, wooden clothespins, a woven laundry basket.",
            "The clothesline stretching between two posts in a garden, lavender bushes below.",
            "A countryside view with rolling hills, a stone wall, puffy clouds in a blue sky."
        ),
        adult_prompt(
            "A stone chapel surrounded by lavender in a quiet valley.",
            "A path of flat stones leading to the chapel entrance, wild lavender growing alongside.",
            "A small Romanesque stone chapel with a bell in a tower, arched doorway, a tiny garden.",
            "A peaceful valley with olive groves, distant mountains, a serene sky."
        ),
        adult_prompt(
            "A candlelit bath scene with lavender floating in the water.",
            "A clawfoot bathtub edge with lavender sprigs floating, bath salts in a jar, a folded towel.",
            "Candles in holders around the tub, a small wooden stool with soap and a loofah.",
            "A bathroom with a small window showing evening sky, shelves with bottles, a plant on a ledge."
        ),
        adult_prompt(
            "A vintage perfume bottle collection with lavender themes.",
            "Ornate glass perfume bottles of various shapes, lavender sprigs, a vanity mirror.",
            "An antique dressing table with a lace runner, a jewelry box, a powder puff.",
            "A bedroom corner with floral wallpaper, a curtained window, a small chandelier."
        ),
        adult_prompt(
            "A farmer's hands tying lavender bundles with twine.",
            "Close-up of hands wrapping twine around a lavender bundle, loose stems, a pair of scissors.",
            "A work table with multiple bundles, a ball of twine, a woven tray.",
            "A barn interior with dried flowers hanging from rafters, farm tools on the wall, warm light."
        ),
        adult_prompt(
            "A rain shower falling on a lavender field with dramatic clouds.",
            "Raindrops on lavender blooms close-up, a puddle reflecting the sky, wet stones on a path.",
            "Lavender rows glistening with rain, a lone umbrella standing upright.",
            "Dramatic storm clouds breaking to reveal a rainbow, distant hills, a wet country road."
        ),
        adult_prompt(
            "A bookshelf decorated with lavender and vintage books.",
            "Old leather-bound books, a small vase of dried lavender, a ceramic figurine of a rabbit.",
            "A tall wooden bookshelf with multiple shelves, a reading lamp, a framed botanical print.",
            "A cozy room with an armchair, a rug, a window with garden view."
        ),
        adult_prompt(
            "A terracotta pot being planted with lavender seedlings.",
            "A large terracotta pot with soil and small lavender plants, gardening trowel, plant labels.",
            "A potting bench with various pots, bags of soil, seed packets.",
            "A greenhouse or potting shed interior with shelves of plants, a watering can, warm light through glass."
        ),
        adult_prompt(
            "A peaceful cemetery gate overgrown with wild lavender.",
            "An old iron gate with ornate scrollwork, wild lavender growing through, a stone step.",
            "A quiet country cemetery with old headstones, a gravel path, ancient trees providing shade.",
            "Rolling countryside beyond the wall, a distant steeple, a calm evening sky."
        ),
        adult_prompt(
            "A Provence balcony with lavender pots and a view of the valley.",
            "Iron railing with potted lavender and geraniums, a cup of espresso, a croissant on a plate.",
            "A stone balcony with a small bistro table and chair, shuttered doors open behind.",
            "A sweeping valley view with patchwork lavender and sunflower fields, a river, distant villages."
        ),
        adult_prompt(
            "A mail carrier's bicycle loaded with lavender bouquets for delivery.",
            "A vintage bicycle with a front basket full of wrapped lavender bouquets, a bell on the handlebar.",
            "A village street with cobblestones, a post box, a bakery with a striped awning.",
            "Village buildings with flower-filled balconies, a church clock tower, a blue sky."
        ),
        adult_prompt(
            "A quiet reading moment in a lavender garden with a hammock.",
            "A book resting on a hammock, a glass of iced tea on a tree stump, a pair of glasses.",
            "A canvas hammock strung between two trees, surrounded by tall lavender bushes.",
            "A cottage with smoke from the chimney, a wooden fence, a sky turning golden at dusk."
        ),
        adult_prompt(
            "A display of lavender products in a Provence shop window.",
            "Bottles of lavender essential oil, sachets, candles, soaps arranged artfully.",
            "A shop window with a wooden frame, a hand-painted sign reading 'Lavande', lace curtains.",
            "A quaint village street with more shops, hanging flower baskets, a cobblestone road."
        ),
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# 20. ENCHANTED FOREST (adults, intricate)
# ─────────────────────────────────────────────────────────────────────────────
BOOKS["enchanted_forest"] = {
    "filename": "20_enchanted_forest.md",
    "theme_key": "enchanted_forest",
    "concept": "Enchanted Forest",
    "audience": "adults",
    "title": "Enchanted Forest: Coloring Book for Adults and Teens",
    "subtitle": "50 Magical Woodland Scenes with Bold and Easy Fairy Doors, Mushroom Circles, and Mystical Creatures",
    "description": (
        "<h4>Step through the fairy door and into a world of magical wonder...</h4><br>"
        "Discover 50 enchanting forest scenes filled with fairy doors hidden in ancient trees, "
        "mystical mushroom circles, owls in moonlit canopies, and enchanted streams. Each page "
        "features bold, easy-to-color outlines with just the right amount of magical detail.<br><br>"
        "<b>What's Inside:</b><br>"
        "&#x2022; 50 unique enchanted forest illustrations<br>"
        "&#x2022; Fairy doors, mushroom villages, magical creatures, ancient trees<br>"
        "&#x2022; Single-sided pages to prevent bleed-through<br>"
        "&#x2022; Large 8.5 x 8.5 inch square pages<br>"
        "&#x2022; Bold outlines perfect for colored pencils, markers, and gel pens<br><br>"
        "<b>Perfect For:</b><br>"
        "&#x2022; Fantasy lovers and nature enthusiasts<br>"
        "&#x2022; Stress relief and creative relaxation<br>"
        "&#x2022; Gift for anyone who loves magical worlds<br>"
        "&#x2022; All skill levels<br><br>"
        "<b>Let the magic of the forest carry you away to a place of calm and wonder.</b>"
    ),
    "keywords": [
        "magical woodland fairy coloring pages fantasy",
        "enchanted forest mushroom fairy door illustration",
        "whimsical nature scenes cottagecore mystical",
        "stress relief creative relaxation art therapy calm",
        "large print simple designs colored pencils markers",
        "gift idea nature lover birthday christmas stocking",
        "bold easy fantasy woodland owl creature aesthetic"
    ],
    "categories": [
        "Crafts, Hobbies & Home / Coloring Books for Grown-Ups / Fantasy & Science Fiction",
        "Crafts, Hobbies & Home / Coloring Books for Grown-Ups / Flowers & Landscapes"
    ],
    "reading_age": "",
    "cover_prompt": (
        "Full-color illustration, magical fantasy forest aesthetic, SQUARE format (1:1 aspect ratio). "
        "A majestic enchanted forest scene with ancient towering trees whose trunks have tiny glowing fairy doors. "
        "A carpet of magical mushrooms with bioluminescent caps covers the forest floor. "
        "Fireflies and fairy lights dance among the branches. A mystical stream winds through with glowing fish. "
        "An owl perches on a branch watching over the scene. Rich jewel tones of emerald, purple, gold, and teal. "
        "Magical dappled light filtering through the canopy. Premium fantasy illustration style. DO NOT include any text in the image."
    ),
    "page_prompts": [
        adult_prompt(
            "An ancient oak tree with a tiny fairy door at its base, surrounded by magical mushrooms.",
            "A carved wooden fairy door with tiny hinges and a doorknob, glowing mushrooms around the roots, scattered acorns.",
            "The massive trunk of a gnarled old oak with twisting roots, moss growing on bark, a small lantern hanging from a low branch.",
            "A misty forest canopy with rays of light filtering through, distant trees fading into fog, ferns covering the ground."
        ),
        adult_prompt(
            "A mushroom circle in a moonlit forest clearing with tiny fairy houses.",
            "Large toadstools forming a perfect circle, tiny windows carved into mushroom caps, a trail of fairy dust.",
            "A clearing with soft moss ground, a tree stump table with acorn cups, fireflies floating around.",
            "Tall dark trees forming a cathedral-like canopy, a full moon visible through a gap, stars twinkling."
        ),
        adult_prompt(
            "A wise owl perched on a branch in a magical canopy of intertwined trees.",
            "A great horned owl with detailed feathers, sitting on a thick branch, a mouse peeking from a knot hole.",
            "Intertwined branches forming natural arches, hanging vines with small flowers, a squirrel on a nearby limb.",
            "The upper canopy with dappled moonlight, moth silhouettes, distant mountains through a break in the trees."
        ),
        adult_prompt(
            "An enchanted stream with stepping stones and glowing lily pads.",
            "Smooth stepping stones across a gentle stream, luminescent lily pads, a frog on a rock.",
            "The stream banks lined with ferns and wildflowers, a fallen log bridge, moss-covered boulders.",
            "Weeping willows trailing into the water, fireflies above the surface, a misty forest backdrop."
        ),
        adult_prompt(
            "A forest gate covered in climbing vines with a mysterious path beyond.",
            "An ornate wrought-iron gate wrapped in flowering vines, a cobblestone path leading through.",
            "Stone pillars on either side of the gate, old lanterns on top, ivy cascading down.",
            "A sunlit forest path curving into the distance beyond the gate, dappled light, ferns lining the way."
        ),
        adult_prompt(
            "A tree house connected by rope bridges in the enchanted canopy.",
            "A rope bridge with wooden planks, hanging lanterns, a small mailbox on a branch.",
            "A whimsical tree house with round windows and a shingled roof, a ladder, a balcony with a railing.",
            "Multiple tree houses visible in the distance connected by bridges, birds nesting, a starry sky through leaves."
        ),
        adult_prompt(
            "A fairy market set up on mushroom shelves in a hollow tree.",
            "Tiny wares on toadstool shelves: bottles of dewdrop potion, acorn caps, crystal shards.",
            "The inside of a massive hollow tree trunk, winding staircase of bark, small lanterns on hooks.",
            "The forest visible through knotholes, roots forming archways, tiny fairy wings visible in corners."
        ),
        adult_prompt(
            "A deer drinking from an enchanted pool that reflects a different scene than reality.",
            "A graceful deer bowing to drink, ripples in the water, fallen leaves on the surface.",
            "A crystal-clear pool surrounded by smooth stones, the reflection showing a castle instead of the forest above.",
            "Ancient trees leaning over the pool, hanging moss, a shaft of golden light hitting the water."
        ),
        adult_prompt(
            "A fox family's den entrance hidden under a mushroom-covered log.",
            "A hollow under a fallen log with a cozy entrance, tiny fox paw prints in the earth, mushrooms growing on the bark.",
            "The fallen log covered in shelf fungi and moss, wildflowers growing alongside, a hedgehog walking past.",
            "Deep forest with towering trees, ferns in layers, shafts of green light."
        ),
        adult_prompt(
            "A forest library inside a giant hollow tree with books on bark shelves.",
            "A reading chair made from twisted roots, open books, a candle in a lantern, reading glasses.",
            "Carved bark shelves lined with tiny books, a winding staircase up the trunk interior, a window shaped like a leaf.",
            "Roots forming the floor, tiny doors leading to other rooms, fairy lights strung along the ceiling."
        ),
        adult_prompt(
            "A magical waterfall with crystalline cave behind it.",
            "Crystals growing from rocks near the base, a treasure chest half-hidden by ferns, sparkles in the mist.",
            "A beautiful waterfall cascading over mossy rocks, the shadow of a cave entrance visible behind the water.",
            "Cliff walls with hanging gardens, birds swooping through the mist, rainbow in the spray."
        ),
        adult_prompt(
            "A gnome's garden with miniature vegetables and tiny tools.",
            "Tiny garden rows with oversized (to gnome scale) cabbages and carrots, a miniature wheelbarrow, a watering can.",
            "A gnome-sized cottage with a red door, a toadstool chimney, a picket fence made of twigs.",
            "The regular-sized forest towering above, a beetle walking by (huge compared to the garden), roots like cliffs."
        ),
        adult_prompt(
            "A spider web decorated with morning dew between two trees.",
            "An intricate spiral spider web with dew drops catching light, a small spider at the center.",
            "Two birch trees with the web strung between them, wildflowers below, a butterfly nearby.",
            "A misty morning forest, sun just rising through the trees, ground mist swirling."
        ),
        adult_prompt(
            "A moonlit clearing where forest animals gather around a glowing stone.",
            "A fox, rabbit, and hedgehog sitting near a softly glowing stone, mushrooms around the clearing edge.",
            "A circle of standing stones in a grassy clearing, fireflies dancing, a fallen oak providing seating.",
            "The dark forest surrounding the clearing, moon directly overhead, stars visible through the canopy gap."
        ),
        adult_prompt(
            "An old forest well with a bucket, surrounded by enchanted flowers.",
            "A stone well with a wooden roof, a bucket on a rope, climbing flowers on the structure.",
            "Magical flowers with oversized petals growing around the well, a cobblestone path, a bench.",
            "Dense enchanted forest behind, ancient trees with face-like bark patterns, gentle fog."
        ),
        adult_prompt(
            "A sleeping dragon curled around a forest tree, small and peaceful.",
            "A small dragon (cat-sized) curled at the base of a tree, wings folded, tail wrapped around itself.",
            "The tree with dragon claw marks on the bark, a nest of leaves, a few scattered scales.",
            "A mystical forest with glowing plants, bioluminescent mushrooms, a twilight sky."
        ),
        adult_prompt(
            "A wooden boat on a still forest lake surrounded by enchanted trees.",
            "A small rowboat with a lantern at the bow, trailing water lilies, an oar resting across.",
            "A mirror-still lake reflecting the surrounding trees perfectly, a dock with a rope.",
            "Enchanted trees with twisted shapes, their canopy creating a tunnel over the water, mist rising."
        ),
        adult_prompt(
            "A fairy ring of flowers with a tiny table set for tea in the center.",
            "A ring of oversized daisies, a tiny table set with acorn cups and leaf plates, a thimble sugar bowl.",
            "The grass inside the ring glowing slightly, a trail of fairy dust leading in, a small toadstool stool.",
            "The dark mysterious forest beyond the ring, ancient trees, a shaft of golden light on the scene."
        ),
        adult_prompt(
            "A forest path with lanterns hanging from low branches guiding the way.",
            "A winding dirt path with small decorative lanterns on shepherd hooks, scattered leaves.",
            "Trees arching over the path forming a natural tunnel, lanterns on hanging hooks, wildflowers along edges.",
            "The path disappearing into a warm glow in the distance, misty forest on both sides, occasional fireflies."
        ),
        adult_prompt(
            "An old forest cabin covered in moss and mushrooms, looking magical.",
            "A wooden cabin with a sagging porch, mushrooms growing from the roof, a rocking chair.",
            "The cabin surrounded by enormous ferns and wildflowers, a stone chimney with gentle smoke.",
            "Deep forest behind, ancient trees with hanging moss, a creek visible to one side."
        ),
        adult_prompt(
            "A magical tree whose leaves are shaped like butterflies.",
            "Branches low enough to see individual butterfly-shaped leaves in detail, some detaching and fluttering.",
            "The full tree with a slender trunk and spreading branches, a carpet of butterfly leaves below.",
            "A meadow clearing with the single magical tree as the centerpiece, surrounding normal trees for contrast."
        ),
        adult_prompt(
            "A hedgehog wearing a tiny hat walking through an enchanted garden.",
            "A cute hedgehog with a small top hat, walking on a path of pebbles, carrying a tiny suitcase.",
            "An enchanted garden with oversized flowers, mushroom lamp posts, a snail mail box.",
            "A miniature village visible in the distance, fairy cottage rooftops, soft warm light."
        ),
        adult_prompt(
            "A hollow stump serving as a woodland post office.",
            "A tree stump with a slot cut for letters, tiny envelopes, a posted sign, a bell.",
            "Birds carrying letters in their beaks, a mailbag hanging from a branch, a sorting shelf inside the stump.",
            "The forest with a path leading to other stumps and mushroom buildings, a woodpecker on a tree."
        ),
        adult_prompt(
            "A forest creek bed with crystals and gemstones visible in the shallow water.",
            "Colorful crystals and smooth gems visible through clear water, a crawfish, pebbles.",
            "A shallow creek with gravel banks, overhanging ferns, roots reaching into the water.",
            "A rocky hillside with exposed crystal formations, trees growing at angles, dappled light."
        ),
        adult_prompt(
            "A caterpillar on a giant mushroom reading a tiny scroll.",
            "A cute caterpillar with expressive eyes sitting on a large mushroom cap, holding a tiny scroll, a monocle.",
            "The large mushroom with a spotted cap, smaller mushrooms around the base, a grass tuft seat.",
            "A whimsical forest with curling ferns, floating dandelion seeds, soft misty background."
        ),
        adult_prompt(
            "A magical greenhouse hidden in the forest with glowing plants.",
            "Glass panels of a greenhouse with condensation, glowing flowers visible inside, a wooden door ajar.",
            "The greenhouse structure covered in vines, stone foundation, small stepping stone path leading to door.",
            "Dense enchanted forest surrounding the structure, tall dark trees, mysterious fog."
        ),
        adult_prompt(
            "A woodland feast laid out on a long table made from a split log.",
            "A long log table with acorn bowls, berry platters, mushroom dishes, nut bread loaves.",
            "Tree stump chairs arranged along both sides, a candelabra of branches, flower decorations.",
            "A festive clearing with hanging lanterns, bunting made of leaves, a campfire glow nearby."
        ),
        adult_prompt(
            "A snowy enchanted forest with ice crystals on every branch.",
            "Detailed ice crystals and snowflakes on branches, frozen berries, icicles hanging.",
            "Snow-covered trees creating a white tunnel, a frozen stream, animal tracks in the snow.",
            "A winter sky with snowflakes falling, pale moonlight, the forest stretching white and silver."
        ),
        adult_prompt(
            "A forest apothecary shelf carved into a cliff face.",
            "Jars and bottles of potions, dried herbs in bundles, crystal balls, a mortar and pestle.",
            "A natural rock shelf carved by time, roots growing around it, moss cushioning the bottles.",
            "A cliff face with water seeping down, ferns growing from crevices, the forest floor below."
        ),
        adult_prompt(
            "An enchanted bridge made entirely of woven tree roots over a ravine.",
            "A detailed bridge of twisted, living roots intertwined, small flowers growing from the roots.",
            "The bridge spanning a mossy ravine, water trickling far below, lanterns on root posts.",
            "Ancient forest on both sides of the ravine, mist rising from below, birds flying through."
        ),
        adult_prompt(
            "A magical compass rose mosaic on a forest floor clearing.",
            "A detailed compass design made of colored leaves, stones, and flowers embedded in the earth.",
            "A circular clearing with the mosaic at center, four paths leading to the four cardinal directions.",
            "Each path disappearing into a different season of forest: spring flowers, summer green, autumn leaves, winter snow."
        ),
        adult_prompt(
            "A fox sitting by a lantern at a crossroads of forest paths.",
            "A red fox sitting elegantly, a warm lantern beside it on the ground, fallen leaves.",
            "A crossroads where three paths meet, a carved wooden signpost with directions, moss-covered stones.",
            "Three different forest paths leading into mystery, each slightly different in character, twilight sky."
        ),
        adult_prompt(
            "A giant ancient tree with a face in its bark, looking wise and kind.",
            "The face in the bark with kind eyes and a gentle expression, moss eyebrows, a bird on its nose.",
            "The massive trunk with face features formed naturally from bark patterns, enormous roots spreading out.",
            "A hushed forest around the tree, smaller trees seeming to lean toward it, golden light."
        ),
        adult_prompt(
            "A forest music scene with woodland creatures playing natural instruments.",
            "A cricket with a tiny violin (leaf), a frog with a drum (mushroom cap), a bird singing on a branch.",
            "A small stage of flat rocks, moss curtains, a log audience seating area.",
            "An evening forest clearing with fireflies as stage lights, stars beginning to appear."
        ),
        adult_prompt(
            "A magical rain in the forest where the drops are tiny crystals.",
            "Crystal raindrops falling onto large leaves, creating small rainbow prisms, puddles with crystal drops.",
            "Trees with their leaves catching crystalline rain, flowers bending under crystal weight.",
            "A misty forest scene with the rain creating a sparkling curtain of light."
        ),
        adult_prompt(
            "An enchanted forest clock tower made from a dead tree trunk.",
            "A clock face built into the side of a tall dead tree, its hands made of branches, mushrooms as numbers.",
            "The tree converted into a tower with spiral bark stairs visible, a bell at the top, small windows.",
            "The living forest surrounding the clock tower, owls perched nearby, a moonlit sky."
        ),
        adult_prompt(
            "A cozy badger's burrow with a fireplace and armchair visible through the entrance.",
            "The entrance to a burrow between tree roots, a doormat, a welcome sign, warm light glowing from inside.",
            "Inside visible: a tiny fireplace, an armchair with a quilt, a bookshelf, a kettle on the hearth.",
            "The forest floor above the burrow with wildflowers, the great roots of a tree, a path leading away."
        ),
        adult_prompt(
            "A flock of magical birds with elaborate tail feathers perched in flowering branches.",
            "Three exotic birds with long decorative tail feathers perched on separate branches, detailed plumage patterns.",
            "Flowering cherry-like branches in full bloom, petals drifting down, a nest visible.",
            "A soft forest background with gentle light, more branches extending, a distant clearing."
        ),
        adult_prompt(
            "A stone circle in the forest with ancient runes carved into each stone.",
            "Detailed standing stones with intricate rune carvings, moss growing in the carved lines, wildflowers at the base.",
            "A circle of seven stones in a clearing, the ground inside covered in soft moss, a central flat stone altar.",
            "Ancient trees surrounding the circle like guardians, a dramatic sky visible through the canopy."
        ),
        adult_prompt(
            "A fairy boat made from a walnut shell sailing on a forest stream.",
            "A walnut shell boat with a leaf sail, a tiny fairy flag, a paddle made from a twig.",
            "A gentle forest stream with the boat floating, water plants along the banks, a jumping fish.",
            "Overhanging branches creating a green tunnel over the stream, dappled light on the water."
        ),
        adult_prompt(
            "A forest observatory platform built in the highest tree.",
            "A wooden platform with a railing, a telescope pointed at the sky, a star chart pinned to a board.",
            "The platform built at the very top of a massive tree, a rope ladder leading down, a hanging lantern.",
            "A panoramic view of the enchanted forest canopy stretching in all directions, a spectacular starry sky above."
        ),
        adult_prompt(
            "A tunnel through a hill covered in tree roots with light at the end.",
            "The entrance to the tunnel framed by tree roots, mushrooms growing on the ceiling, small crystals in the walls.",
            "The tunnel interior with a path of smooth stones, roots creating natural arches, gentle dripping water.",
            "A bright enchanted clearing visible at the far end, warm golden light streaming in."
        ),
        adult_prompt(
            "A magical garden where flowers are as tall as trees.",
            "Gigantic daisy stems thick as tree trunks, petals the size of umbrellas, a beetle climbing a stem.",
            "A path winding between massive flower stalks, a swing hanging from a stem, fallen petals as stepping stones.",
            "The garden stretching with more giant flowers, a tiny cottage at ground level, clouds near the flower tops."
        ),
        adult_prompt(
            "A winged cat sleeping in a nest of leaves high in a tree.",
            "A small cat with folded butterfly wings curled in a nest of autumn leaves, a feather tucked nearby.",
            "A tree branch with the nest in a natural fork, acorns stored alongside, a carved name on the bark.",
            "The treetop with a view of the forest, other nests visible in distant trees, a twilight sky."
        ),
        adult_prompt(
            "An enchanted forest map carved into a flat stone by a path.",
            "A detailed map carved into a large flat stone showing paths, landmarks, and a 'you are here' mark.",
            "The stone set beside a crossroads, moss growing around edges, a walking stick leaning against it.",
            "The forest paths matching the map's routes, various landmarks visible in the distance."
        ),
        adult_prompt(
            "A forest hot spring surrounded by mossy rocks and enchanted plants.",
            "Steam rising from a natural hot spring, smooth stones for sitting, a folded towel on a rock.",
            "The hot spring pool surrounded by mossy boulders, glowing plants at the edges, a tiny waterfall feeding it.",
            "Dense enchanted forest, tall ferns, the steam creating a magical misty atmosphere."
        ),
        adult_prompt(
            "Autumn in the enchanted forest with magical falling leaves that glow.",
            "Glowing golden and amber leaves falling in spirals, some collecting on the ground, a mushroom ring.",
            "Trees in full autumn color with leaves releasing and floating, a pathway covered in golden leaves.",
            "A spectacular canopy of reds, oranges, and golds, shafts of warm light, the forest in its glory."
        ),
        adult_prompt(
            "A tiny dragon hatching from an egg in a nest of gems and crystals.",
            "A small dragon egg cracking open, a baby dragon peaking out with big eyes, scattered crystal shards.",
            "A nest made of woven branches lined with gems and crystals, other eggs waiting, warm glow.",
            "A hidden cave under a tree root, the forest visible through the entrance, protective mother dragon's tail visible."
        ),
        adult_prompt(
            "A forest mailbox shaped like an owl with letters sticking out.",
            "A carved wooden owl mailbox with a hinged beak, letters and scrolls protruding, a small flag up.",
            "The mailbox on a post at a path junction, a bench nearby, flower boxes on both sides.",
            "A path leading deeper into the enchanted forest, lampposts with candles, distant fairy lights."
        ),
    ],
}

# Helper to generate remaining books efficiently
# I'll define each book's data compactly

# ─────────────────────────────────────────────────────────────────────────────
# 21. FERN & MOSS WOODLAND (adults)
# ─────────────────────────────────────────────────────────────────────────────
BOOKS["fern_moss_woodland"] = {
    "filename": "21_fern_moss_woodland.md",
    "theme_key": "fern_moss_woodland",
    "concept": "Fern & Moss Woodland",
    "audience": "adults",
    "title": "Fern & Moss Woodland: Coloring Book for Adults, Bold and Easy",
    "subtitle": "50 Serene Forest Floor Scenes with Ferns, Mossy Stones, and Peaceful Nature Designs for Relaxation",
    "description": (
        "<h4>Find peace in the quiet beauty of the forest floor...</h4><br>"
        "Immerse yourself in 50 tranquil woodland scenes celebrating the delicate world of ferns, "
        "moss-covered stones, and lush forest undergrowth. Each page captures the hushed serenity "
        "of nature's green carpet with bold, satisfying outlines.<br><br>"
        "<b>What's Inside:</b><br>"
        "&#x2022; 50 unique fern and moss woodland illustrations<br>"
        "&#x2022; Unfurling fiddleheads, mossy boulders, forest streams, mushrooms, lichen patterns<br>"
        "&#x2022; Single-sided pages to prevent bleed-through<br>"
        "&#x2022; Large 8.5 x 8.5 inch square pages<br>"
        "&#x2022; Bold outlines perfect for colored pencils, markers, and gel pens<br><br>"
        "<b>Perfect For:</b><br>"
        "&#x2022; Nature lovers and forest bathing enthusiasts<br>"
        "&#x2022; Mindful relaxation and stress relief<br>"
        "&#x2022; Gift for hikers, botanists, and green thumbs<br>"
        "&#x2022; All skill levels<br><br>"
        "<b>Step onto the soft moss and let the woodland calm your mind.</b>"
    ),
    "keywords": [
        "fern moss forest floor botanical illustration",
        "woodland nature coloring pages green peaceful",
        "forest bathing shinrin yoku mindfulness calm",
        "stress relief relaxation art therapy creative",
        "large print simple designs colored pencils markers",
        "gift idea nature hiker botanist birthday christmas",
        "bold easy botanical undergrowth lichen fungi"
    ],
    "categories": [
        "Crafts, Hobbies & Home / Coloring Books for Grown-Ups / Flowers & Landscapes",
        "Crafts, Hobbies & Home / Coloring Books for Grown-Ups / General"
    ],
    "reading_age": "",
    "cover_prompt": (
        "Full-color illustration, serene nature aesthetic, SQUARE format (1:1 aspect ratio). "
        "A lush forest floor scene with unfurling fern fiddleheads in the foreground, moss-covered boulders "
        "and fallen logs in the middle ground, and tall ancient trees with filtered green light in the background. "
        "Dappled sunlight creates golden patches on the moss. A small stream trickles between rocks. "
        "Shelf fungi grow on a log. Rich greens, emeralds, and golden browns. Peaceful, meditative mood. "
        "DO NOT include any text in the image."
    ),
    "page_prompts": [],  # Will be filled by generator function
}


def generate_fern_moss_prompts():
    """Generate 50 prompts for Fern & Moss Woodland."""
    scenes = [
        ("A fern fiddlehead unfurling in close-up detail on the forest floor.",
         "A large spiraling fiddlehead with fuzzy coating, smaller fiddleheads at different stages, fallen bark.",
         "Forest floor with various fern species at different heights, a mossy log, a small beetle.",
         "Tall tree trunks fading into soft light, a canopy filtering dappled sunshine."),
        ("A moss-covered stone wall in an ancient woodland.",
         "Thick cushion moss on old stones, small ferns growing from cracks, a snail on the wall.",
         "A crumbling stone wall stretching into the distance, ivy and lichen patterns, fallen stones.",
         "Dense woodland behind the wall, tall trees, a gentle mist."),
        ("A forest stream flowing over mossy rocks.",
         "Smooth river stones with thick green moss, water pooling in hollows, fallen leaves floating.",
         "A gentle stream winding between mossy boulders, ferns leaning over the water, a small cascade.",
         "Dense forest on both banks, tall trees reflected in still pools, dappled light."),
        ("A fallen tree trunk covered in shelf fungi and moss.",
         "Large shelf fungi (bracket fungi) in tiers on a log, moss carpet, small sprouting seedlings.",
         "A massive fallen tree with exposed root ball, the trunk creating a bridge over a dip.",
         "A clearing created by the fallen tree, new growth reaching for light, birds on branches above."),
        ("A fern grotto beside a small waterfall.",
         "Maidenhair ferns hanging from dripping rock, water droplets on fronds, a smooth wet stone.",
         "A small waterfall cascading into a grotto pool, ferns of multiple varieties lining the walls.",
         "Rocky overhang with tree roots dangling, the forest visible beyond the grotto entrance."),
        ("A tree trunk entirely covered in green moss, creating a pillar of green.",
         "The base of a moss-covered trunk with details of different moss species, a mushroom cluster.",
         "The full trunk sheathed in emerald moss, a woodpecker hole, lichen patches of grey and yellow.",
         "The forest canopy above, other trees for scale, shafts of light hitting the moss."),
        ("A carpet of moss covering a forest clearing like a green lawn.",
         "Close-up moss carpet with tiny spore capsules standing up, a ladybug crawling, dewdrops.",
         "The moss clearing stretching flat and green, bordered by fern patches, a fallen branch.",
         "Tall trees surrounding the clearing like walls, a break in the canopy showing sky."),
        ("A spiral of fern fronds viewed from above forming a natural pattern.",
         "Multiple fern fronds radiating from a central point in a spiral pattern, each frond detailed.",
         "The base of a large fern plant, smaller plants around it, moss ground.",
         "The forest floor extending outward, other ferns, logs, and stones in natural arrangement."),
        ("A mossy log bridge over a quiet forest stream.",
         "The end of a fallen log used as a bridge, thick moss on top, a bracket fungus step.",
         "The log spanning a narrow stream, ferns below, moss hanging from the underside.",
         "A peaceful stream scene with reflections, the forest continuing on both sides."),
        ("A lichen-covered rock face with intricate patterns.",
         "Detailed lichen patterns in circles and patches on rock, different species in different textures.",
         "A tall rock face with layered lichen growth, small ferns in crevices, dripping water.",
         "A forest backdrop with the rock as a focal point, trees growing close, filtered light."),
        ("A hollow log serving as a natural planter for ferns.",
         "A hollow log section with ferns growing from the decaying interior, mushrooms on the outer bark.",
         "The log resting on the forest floor, surrounded by leaf litter and smaller plants.",
         "A shaded woodland scene with dappled light, tall trees, ground fog."),
        ("A tree root system exposed on a hillside covered in moss.",
         "Massive roots reaching out and down the hillside, moss coating each root, small caves between roots.",
         "The tree standing atop the hill with enormous spreading roots, a path winding between them.",
         "The hillside forest with layers of vegetation, ferns growing in the root network."),
        ("A patch of different moss species growing together like a tapestry.",
         "Sphagnum moss, cushion moss, and hair cap moss growing in distinct patches, tiny spore stalks.",
         "A shaded area under a tree where multiple moss species thrive, a rotting stump, a pinecone.",
         "The forest canopy providing shade, tree trunks, a peaceful understory."),
        ("A stone stairway in the forest covered in moss and ferns.",
         "Old stone steps with moss filling every crack, fern fronds reaching across, a walking stick propped.",
         "A winding stairway carved into a hillside, fern walls on both sides, a handrail of roots.",
         "The stairway disappearing upward into mist, tall trees flanking, a filtered light."),
        ("A forest pond edge with aquatic ferns and moss-covered stones.",
         "Pond edge with floating aquatic ferns, round mossy stones, a water strider on the surface.",
         "A still forest pond reflecting trees, lily pads and ferns, a log partially submerged.",
         "Dense forest surrounding the pond, tall reeds on one side, a heron in the distance."),
        ("A mushroom cluster growing from a mossy stump.",
         "A group of delicate mushrooms with detailed gills and caps, growing from deep green moss, spores visible.",
         "A tree stump covered in moss serving as the mushroom garden, bark peeling, a slug nearby.",
         "A dark forest floor with scattered leaves, other stumps visible, soft filtered light."),
        ("A giant fern canopy viewed from below looking up.",
         "The undersides of massive tree fern fronds with detailed patterns, a few spiders hanging.",
         "Multiple fern canopy layers creating a green ceiling, tree trunks rising through, epiphytes on trunks.",
         "Glimpses of sky through the fern canopy, a tropical-feeling understory, filtered green light."),
        ("A mossy bird bath in a secret garden clearing.",
         "A stone bird bath thick with moss, water with floating moss bits, a robin bathing.",
         "The clearing with the bird bath as centerpiece, ferns in organized rings, stepping stones.",
         "A wall of forest around the clearing, a gate visible, climbing ivy on old stones."),
        ("A forest floor cross-section showing roots, fungi, and underground life.",
         "A natural cutaway showing tree roots intertwined, fungal mycelium networks, an earthworm.",
         "The cross-section of earth showing layers: leaf litter, humus, roots, stones, underground life.",
         "Above ground: the forest floor with ferns and moss continuing naturally."),
        ("A rotting log in decomposition stages with new life growing from it.",
         "The end of a crumbling log with visible decay, new seedlings sprouting, bright green moss.",
         "The log in stages from intact to decomposed along its length, different fungi and plants at each stage.",
         "A regenerating forest area with new and old growth mixing, light reaching the floor."),
        ("A fern-filled ravine with a rope bridge above.",
         "Dense ferns filling the ravine bottom, a stream trickling through, stones with moss.",
         "A rope bridge spanning the ravine above, the ravine walls covered in ferns and moss.",
         "The forest at the ravine rim, trees leaning over, misty atmosphere."),
        ("A stone cottage wall being slowly claimed by moss and ferns.",
         "A close-up of an old stone wall with mortar gaps filled with moss, ferns sprouting from joints.",
         "The wall of a long-abandoned cottage, a window frame with no glass, ferns growing inside.",
         "The forest reclaiming the structure, trees growing through the roof, nature winning."),
        ("A close-up of lichen on a branch showing its fractal patterns.",
         "Detailed lichen growth on a branch showing circular patterns, multiple species, tiny structures.",
         "The branch against a blurred forest background, other lichened branches, a bird perched far away.",
         "A soft focus forest backdrop, gentle light highlighting the lichen details."),
        ("A forest path after rain with puddles reflecting the fern canopy.",
         "Rain puddles on a dirt path reflecting ferns and sky, wet leaves, a snail crossing.",
         "A winding path through dense fern growth, the ferns wet and dripping, a mist rising.",
         "The forest after rain with everything glistening, heightened greens, fresh atmosphere."),
        ("A moss terrarium in a glass jar sitting on a forest stump.",
         "A large glass jar containing a miniature moss landscape, tiny stones, a small fern, condensation.",
         "A tree stump serving as a table, the jar as centerpiece, a few acorns, a butterfly on the rim.",
         "The real forest beyond matching the terrarium's contents on a grand scale."),
        ("A woodpecker hole in a moss-covered tree with a peek inside.",
         "A round hole in a mossy trunk, a woodpecker peeking out, wood chips below, a feather.",
         "The moss-sheathed tree trunk with the hole, other holes visible, bark texture under moss.",
         "The forest around the tree, other trees, ferns at the base, dappled light."),
        ("A natural stone arch covered in moss with ferns hanging.",
         "A stone arch formed naturally, thick moss covering every surface, ferns trailing down like curtains.",
         "The arch spanning a small path, water dripping from the apex, stones underfoot.",
         "The forest visible through the arch, inviting and mysterious, golden light beyond."),
        ("A bog landscape with sphagnum moss hummocks and tiny sundew plants.",
         "Sphagnum moss mounds in detail, tiny sundew plants with dewdrop tentacles, a cranberry vine.",
         "A boggy landscape with moss hummocks, small pools of dark water, sedges and rushes.",
         "A sparse tree line of birch and pine, a wide sky, distant forest edge."),
        ("A forest staircase made from flat stones, each covered in different moss.",
         "Flat stepping stones with varied moss types, each a different shade of green, tiny flowers between.",
         "A natural staircase climbing a gentle slope, bordered by ferns, a handrail of braided roots.",
         "The forest above the slope, the destination a sunlit clearing, birds singing."),
        ("A nurse log with dozens of seedlings growing from it.",
         "A decomposing log with rows of tiny seedling trees sprouting, each with a few leaves, moss substrate.",
         "The full nurse log with hemlock and cedar seedlings in a line, their roots gripping the bark.",
         "A mature forest showing what these seedlings will become, the cycle of forest life."),
        ("A mossy stone meditation circle in the forest.",
         "Smooth moss-covered stones arranged in a circle, a flat center stone, a feather, a pinecone.",
         "The circle in a quiet forest glade, soft moss ground inside, ferns marking the border.",
         "Tall silent trees around the glade, soft light, a feeling of deep peace."),
        ("A close-up of moss spore capsules on their stalks.",
         "Detailed spore capsules on thin red stalks, hundreds in a cluster, each with a cap, tiny scale.",
         "The moss mat from which the spores rise, texture of the moss surface, a water drop.",
         "Blurred forest background, the tiny world presented in magnificent detail."),
        ("A forest swing hanging from an old oak, landing area covered in moss.",
         "A rope swing with a wooden seat, resting on soft moss, a trail of foot scrapes in the moss.",
         "The swing hanging from a massive oak branch, the rope worn smooth, wildflowers growing nearby.",
         "A peaceful forest clearing, the oak as guardian, afternoon sunlight, distant path."),
        ("A waterfall behind a curtain of maidenhair ferns.",
         "Delicate maidenhair fern fronds in a curtain, water visible through them, mist droplets.",
         "A medium waterfall cascading behind the fern curtain, wet rocks, a shallow pool at base.",
         "A rocky grotto setting, the waterfall's source above, lush vegetation all around."),
        ("A fallen acorn sprouting on a moss bed.",
         "A single acorn with its cap nearby, a tiny sprout emerging, resting on deep moss, a dew drop.",
         "The moss bed stretching around, other acorns scattered, a dead leaf curled nearby.",
         "The parent oak tree towering above, its massive trunk, the promise of new life below."),
        ("A forest boulder with a natural garden growing on top.",
         "The top of a large boulder with a miniature garden: moss, ferns, a tiny tree, lichen patterns.",
         "The boulder in a stream, water flowing around it, other rocks with similar gardens.",
         "A forest stream scene, trees lining the banks, a natural bridge downstream."),
        ("A pair of hiking boots covered in mud, resting on moss by a trail.",
         "Well-worn hiking boots with mud and leaf debris, untied laces, resting on thick cushion moss.",
         "A forest trail marker, a resting spot with a flat rock, a water bottle and map nearby.",
         "A forest trail disappearing into fern-lined depths, inviting further exploration."),
        ("A bird's nest made of moss sitting in a fern frond.",
         "A small woven nest incorporating green moss, three tiny eggs, tucked into the curl of a fern.",
         "The fern frond supporting the nest, other fronds providing cover, a parent bird approaching.",
         "The forest understory, protective fern coverage, soft filtered light."),
        ("A stream-side fern garden with a small wooden footbridge.",
         "Ferns growing lush beside a stream, a simple wooden plank bridge, moss on the bridge rails.",
         "The stream flowing gently, the bridge crossing at the narrowest point, wildflowers on the far bank.",
         "A leafy forest backdrop, the stream disappearing around a mossy bend."),
        ("A sunbeam hitting a single fern frond, making it glow.",
         "A single fern frond perfectly lit by a shaft of sunlight, every leaflet illuminated, glowing green.",
         "The surrounding ferns in shadow for contrast, the sunbeam visible as a diagonal line of light.",
         "The dark forest creating the contrast, a single beam breaking through the canopy."),
        ("A moss-covered stone fountain in an overgrown formal garden.",
         "A tiered stone fountain thick with moss, water barely trickling, ferns growing from the bowls.",
         "An overgrown garden with the fountain at center, paths barely visible under vegetation.",
         "Old garden walls, topiary shapes lost under growth, the forest creeping in from outside."),
        ("A tree trunk with peeling bark revealing patterns beneath, moss filling gaps.",
         "Birch bark peeling in sheets, underneath patterns exposed, moss growing in the exposed areas.",
         "The tree trunk showing multiple stages of bark shedding, each layer different, lichen and moss.",
         "A birch forest with multiple trunks showing similar patterns, a uniform understory."),
        ("A forest fairy circle of darker green moss in a clearing.",
         "A perfect ring of darker, lusher moss in a lighter moss clearing, small mushrooms at the ring edge.",
         "The clearing with the fairy circle as the clear focus, no one there but the suggestion of magic.",
         "The dark forest surrounding the clearing, ancient trees watching, a mysterious light."),
        ("A close-up of bracket fungi stacked on a mossy trunk.",
         "Multiple shelf fungi (Ganoderma or Turkey Tail) in a staircase pattern, detailed cap patterns.",
         "The moss-covered tree trunk serving as substrate, bark visible between fungi, a beetle on one cap.",
         "The dark forest floor, the trunk as a vertical element, soft green ambient light."),
        ("A forest creek crossing with stepping stones covered in wet moss.",
         "Large flat stones placed as steps across the creek, each with slippery-looking moss, water flowing around.",
         "The creek with clear water showing pebbles below, ferns on both banks, a fallen branch.",
         "The forest stretching along the creek, bending trees, a path continuing on the far side."),
        ("A secret garden door hidden behind hanging fern curtains.",
         "Fern fronds hanging like a curtain, partially revealing an old wooden door with iron hardware.",
         "A stone wall almost invisible behind ferns and moss, the door set into it, a worn path leading to it.",
         "The forest pressing close, the secret door an invitation to wonder, soft glowing light around the edges."),
        ("A rain-soaked forest with every surface glistening and mossy.",
         "Close-up of rain-soaked moss with water droplets like jewels, a centipede curling, wet bark.",
         "The forest in full saturation after rain, every surface green and glistening, a steaming log.",
         "A moody forest atmosphere, low clouds visible through trees, the beauty of the wet world."),
        ("A forest stump serving as a reading desk with a book and lantern.",
         "A flat-topped stump with an open book, a lantern with a candle, a cup of something warm.",
         "The stump surrounded by soft moss, a cushion placed on it, ferns creating privacy.",
         "A quiet corner of the forest, perfect for contemplation, golden warm light from the lantern."),
        ("A winter forest with moss still green under a thin layer of snow.",
         "Snow dusting on moss, the green still visible beneath, ice crystals on fern fronds.",
         "A winter woodland with bare branches, evergreen moss and ferns the only color, frost on logs.",
         "A pale winter sky, bare tree silhouettes, the resilient green of moss in winter."),
        ("A tiny waterfall trickling down a moss-covered rock face into a pool.",
         "Water trickling over thick moss on a rock face, each trickle path defined, a tiny pool below.",
         "The rock face in detail with layers of moss, ferns growing from ledges, a small cave behind the water.",
         "A shaded forest alcove, the waterfall creating a peaceful sound, ferns everywhere."),
    ]
    return [adult_prompt(*s) for s in scenes]


BOOKS["fern_moss_woodland"]["page_prompts"] = generate_fern_moss_prompts()


def save_book(theme_key, data):
    """Save a book's plan.json and prompts.txt."""
    out_dir = os.path.join(OUTPUT_DIR, theme_key)
    os.makedirs(out_dir, exist_ok=True)

    plan = {
        "theme_key": theme_key,
        "concept": data["concept"],
        "audience": data["audience"],
        "page_size": PAGE_SIZE,
        "title": data["title"],
        "subtitle": data["subtitle"],
        "description": data["description"],
        "keywords": data["keywords"],
        "author": AUTHOR,
        "cover_prompt": data["cover_prompt"],
        "page_prompts": data["page_prompts"],
        "categories": data["categories"],
        "reading_age": data["reading_age"],
    }

    # Save plan.json
    plan_path = os.path.join(out_dir, "plan.json")
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    # Save prompts.txt
    prompts_path = os.path.join(out_dir, "prompts.txt")
    with open(prompts_path, "w") as f:
        for p in data["page_prompts"]:
            f.write(p + "\n")

    # Move idea to done
    idea_file = os.path.join(IDEAS_DIR, data["filename"])
    done_file = os.path.join(DONE_DIR, data["filename"])
    if os.path.exists(idea_file):
        shutil.move(idea_file, done_file)

    return plan_path


if __name__ == "__main__":
    import sys

    # Process all defined books
    count = 0
    for theme_key, data in BOOKS.items():
        if len(data.get("page_prompts", [])) == PAGE_COUNT:
            path = save_book(theme_key, data)
            count += 1
            print(f"[{count}] Saved: {path} ({len(data['page_prompts'])} prompts)")
        else:
            print(f"SKIP: {theme_key} - has {len(data.get('page_prompts', []))} prompts (need {PAGE_COUNT})")

    print(f"\nTotal saved: {count} books")
