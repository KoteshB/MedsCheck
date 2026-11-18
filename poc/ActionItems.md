# Action items: medicines not in the list

Context: `medcheck-minimal-2.html` only accepts medicines picked from the suggestion list. The built-in list has about 190 names, so many real medicines are missing. These items cover how the page and backend should handle that.

## 1. Use a bigger medicine source

- Set `USE_NLM = true` to use the NLM RxTerms list, or serve suggestions from our own backend (RxNorm).
- Serving from the backend lets us control privacy: typed text does not go to an outside service.
- Add brand names and non-US names (e.g. Paracetamol, Salbutamol).
- See `References.html` for what RxNorm is.

## 2. Show a clear "no match" state

- Keep "No matching medicine found. Check the spelling."
- Add "Did you mean…" using fuzzy matching, because drug names are often mistyped.
- RxNorm has an approximate-match service that can do this.

## 3. Offer "Add as typed", flagged as unverified

- Let the user add text that is not in the list (regional brand, herbal product, supplement).
- Show it as a different chip (e.g. dashed border, "unverified").
- Send it to the backend, which reports "I am unable to find the answer" for it.
- **Decision needed:** this changes the current rule "only pick from suggestions". Strict (current) keeps data clean but can block users with uncommon medicines.

## 4. Never let an unknown entry look checked

- The results must say, for each medicine, whether it was checked or not checked.
- Never show "no interactions found" without making clear which medicines were covered.
- Send the user to a pharmacist for any medicine that was not checked.

## 5. Do not ask the model to guess

- An unrecognized name must not go to the LLM for a best guess.
- It either matches a source record, or it is reported as "unable to find".
- This follows the design rules in `CLAUDE.md` and `docs/design-decisions.md`.

## Suggested order

1. Larger source (item 1)
2. "Add as typed" with the unverified chip (item 3)
3. Checked / not checked line in the results (item 4)
4. "Did you mean…" (item 2)
5. Keep item 5 as a rule throughout

## Related

- Backend still accepts any number of medicines. The page caps the list at 25, so add a matching check in `poc/api`.
