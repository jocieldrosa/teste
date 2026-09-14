resultado = cv2.matchTemplate(tela, template, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

print(f"Confiança máxima encontrada: {max_val}")