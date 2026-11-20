-- SPDX-License-Identifier: CC-BY-SA-4.0
-- Adapted from the MISP Book PDF filter. See assets/README.md for attribution.
-- Quarto resolves most PDF links, but some chapter links retain their .qmd path.
local chapter_ids = {}

local function record_chapter(header)
  local metadata = quarto.doc.file_metadata()
  local file = metadata and metadata.file
  if header.level == 1 and file and file.bookItemFile and file.bookItemType ~= 'part' then
    local path = file.bookItemFile
    chapter_ids[path] = chapter_ids[path] or header.identifier
  end
end

local function link_chapters(doc)
  return doc:walk({
    Link = function(link)
      local path, fragment = link.target:match('^([^#]+)#?(.*)$')
      if not path or not path:match('%.qmd$') or path:match('^%a[%w+.-]*:') then return end
      -- Chapter paths are relative to the root or one directory below it.
      path = path:gsub('^%./', ''):gsub('^%.%./', '')
      local id = chapter_ids[path]
      if id and id ~= '' then
        link.target = '#' .. (fragment ~= '' and fragment or id)
        return link
      end
    end,
  })
end

return quarto.utils.combineFilters({
  quarto.utils.file_metadata_filter(),
  { Header = record_chapter, Pandoc = link_chapters },
})
